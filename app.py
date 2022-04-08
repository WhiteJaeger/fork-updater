import datetime
import os
from subprocess import run, CompletedProcess

from flask import Flask, render_template, request, json, flash, url_for, redirect
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import check_password_hash

from constants import (UPSTREAM_REPO_URL,
                       CURRENT_DIR,
                       PATH_TO_SCRIPTS,
                       GH_USER,
                       UpdateStrategyMessages,
                       LOGGER,
                       SyncStatusMessages)
from db import get_forks_from_db, sync_forks_list_with_github, get_db, get_user_by_email, get_user_by_id
from models import User
from utils import generate_random_string


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    with app.app_context():
        with open(os.path.join(CURRENT_DIR, 'schema.sql')) as f:
            db = get_db()
            db.executescript(f.read())
            db.commit()

        @login_manager.user_loader
        def load_user(user_id: int):
            return get_user_by_id(user_id)

    return app


APP = create_app()


@APP.route('/')
@login_required
def home():
    forks = get_forks_from_db()
    return render_template('home.html', forks=forks, upstream=UPSTREAM_REPO_URL)


@APP.route('/update', methods=['POST'])
@login_required
def update_fork():
    data = json.loads(request.get_data().decode('utf-8'))
    fork_url = data.get('url')
    update_strategy = data.get('strategy')
    random_string = generate_random_string()
    args = [random_string, fork_url, UPSTREAM_REPO_URL, GH_USER, update_strategy]

    rc: CompletedProcess = run([os.path.join(PATH_TO_SCRIPTS, 'update.sh'), *args], capture_output=True)

    stdout = rc.stdout.decode('utf-8')
    LOGGER.debug(stdout)

    stderr = rc.stderr.decode('utf-8')
    LOGGER.debug(stderr)

    result = {'returnCode': str(rc.returncode)}

    if rc.returncode == 0:
        cur_time = datetime.datetime.now().ctime()

        update_status = None
        if update_strategy == UpdateStrategyMessages.getNew.name:
            update_status = str(UpdateStrategyMessages.getNew)
        elif update_strategy == UpdateStrategyMessages.keepFork.name:
            update_status = str(UpdateStrategyMessages.keepFork)
        elif update_strategy == UpdateStrategyMessages.keepUpstream.name:
            update_status = str(UpdateStrategyMessages.keepUpstream)

        db = get_db()
        db.execute('UPDATE forks SET updateStatus = ?, lastUpdateTime = ? WHERE url = ?',
                   (update_status, cur_time, fork_url))
        db.commit()

        result['updateStatus'] = update_status
        result['lastUpdateTime'] = cur_time

    return json.dumps(result)


@APP.route('/update-fork-status', methods=['POST'])
@login_required
def update_fork_status():
    data = json.loads(request.get_data().decode('utf-8'))
    fork_url = data.get('url')
    random_string = generate_random_string()
    args = [random_string, fork_url, UPSTREAM_REPO_URL, GH_USER]
    rc: CompletedProcess = run([os.path.join(PATH_TO_SCRIPTS, 'check_if_fork_has_conflict.sh'), *args],
                               capture_output=True)

    stdout = rc.stdout.decode('utf-8')
    LOGGER.debug(stdout)

    stderr = rc.stderr.decode('utf-8')
    LOGGER.debug(stderr)

    # 0 - no conflict, 1 - conflict
    result = {'returnCode': str(rc.returncode)}
    if rc.returncode != 0 and rc.returncode != 1:
        return 'UNKNOWN RETURN CODE!'

    cur_time = datetime.datetime.now().ctime()
    db = get_db()

    if rc.returncode == 0:

        db.execute('UPDATE forks SET syncStatus = ?, lastSyncTime = ? WHERE url = ?',
                   ('No conflict', cur_time, fork_url))
        result['syncStatus'] = str(SyncStatusMessages.no_conflict)
    elif rc.returncode == 1:
        db.execute('UPDATE forks SET syncStatus = ?, lastSyncTime = ? WHERE url = ?',
                   ('Conflict', cur_time, fork_url))
        result['syncStatus'] = str(SyncStatusMessages.conflict)

    db.commit()
    result['lastSyncTime'] = cur_time
    return json.dumps(result)


@APP.route('/sync-forks-with-github', methods=['GET'])
@login_required
def sync_forks_with_github():
    sync_forks_list_with_github()
    return json.dumps({'result': 'ok'})


@APP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            login_user(User(user['id'], user['email'], user['password']))
            return redirect(url_for('home'))
        else:
            flash('Incorrect email and/or password!')
            return render_template('login.html')

    return render_template('login.html')


if __name__ == '__main__':
    APP.run()
