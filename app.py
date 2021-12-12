import datetime
import os
from subprocess import run, CompletedProcess

from flask import Flask, render_template, request, json

from constants import UPSTREAM_REPO_URL, CURRENT_DIR, PATH_TO_LOG_FILE, PATH_TO_ERROR_LOG_FILE, GH_USER, UpdateStrategy
from db import get_forks_from_db, sync_forks_list_with_github, get_db
from utils import generate_random_string, write_log


def create_app():
    app = Flask(__name__)
    with app.app_context():
        with open(os.path.join(CURRENT_DIR, 'schema.sql')) as f:
            db = get_db()
            db.executescript(f.read())
            db.commit()
            db.close()
    return app


APP = create_app()


@APP.route('/')
def home():
    forks = get_forks_from_db()
    return render_template('home.html', forks=forks, upstream=UPSTREAM_REPO_URL)


@APP.route('/update', methods=['POST'])
def update_fork():
    data = json.loads(request.get_data().decode('utf-8'))
    fork_url = data.get('url')
    update_strategy = data.get('strategy')
    random_string = generate_random_string()
    args = [random_string, fork_url, UPSTREAM_REPO_URL, GH_USER, update_strategy]

    rc: CompletedProcess = run([os.path.join(CURRENT_DIR, 'update.sh'), *args], capture_output=True)

    stdout = rc.stdout.decode('utf-8')
    write_log(PATH_TO_LOG_FILE, stdout)

    stderr = rc.stderr.decode('utf-8')
    write_log(PATH_TO_ERROR_LOG_FILE, stderr)

    result = {'returnCode': str(rc.returncode)}

    if rc.returncode == 0:
        cur_time = datetime.datetime.now().ctime()

        update_status = 'Updated with strategy: '
        if update_strategy == UpdateStrategy.getNew.name:
            update_status += UpdateStrategy.getNew.value
        elif update_strategy == UpdateStrategy.keepFork.name:
            update_status += UpdateStrategy.keepFork.value
        elif update_strategy == UpdateStrategy.keepUpstream.name:
            update_status += UpdateStrategy.keepUpstream.value

        db = get_db()
        db.execute('UPDATE forks SET updateStatus = ?, lastUpdateTime = ? WHERE url = ?',
                   (update_status, cur_time, fork_url))
        db.commit()
        db.close()

        result['updateStatus'] = update_status
        result['lastUpdateTime'] = cur_time

    return json.dumps(result)


@APP.route('/update-fork-status', methods=['POST'])
def update_fork_status():
    data = json.loads(request.get_data().decode('utf-8'))
    fork_url = data.get('url')
    random_string = generate_random_string()
    args = [random_string, fork_url, UPSTREAM_REPO_URL, GH_USER]
    rc: CompletedProcess = run([os.path.join(CURRENT_DIR, 'check_if_fork_has_conflict.sh'), *args], capture_output=True)

    stdout = rc.stdout.decode('utf-8')
    write_log(PATH_TO_LOG_FILE, stdout)

    stderr = rc.stderr.decode('utf-8')
    write_log(PATH_TO_ERROR_LOG_FILE, stderr)

    # 0 - no conflict, 1 - conflict
    result = {'returnCode': str(rc.returncode)}
    if rc.returncode != 0 and rc.returncode != 1:
        return 'UNKNOWN RETURN CODE!'

    cur_time = datetime.datetime.now().ctime()
    db = get_db()

    if rc.returncode == 0:

        db.execute('UPDATE forks SET syncStatus = ?, lastSyncTime = ? WHERE url = ?',
                   ('No conflict', cur_time, fork_url))
        result['syncStatus'] = 'No conflict'
    elif rc.returncode == 1:
        db.execute('UPDATE forks SET syncStatus = ?, lastSyncTime = ? WHERE url = ?',
                   ('Conflict', cur_time, fork_url))
        result['syncStatus'] = 'Conflict'

    db.commit()
    db.close()
    result['lastSyncTime'] = cur_time
    return json.dumps(result)


@APP.route('/sync-forks-with-github', methods=['POST'])
def sync_forks_with_github():
    sync_forks_list_with_github()
    return json.dumps({'result': 'ok'})


if __name__ == '__main__':
    APP.run()
