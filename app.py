import os
from subprocess import run, CompletedProcess

from flask import Flask, render_template, request, json

from constants import UPSTREAM_REPO_URL, CURRENT_DIR
from db import get_forks_from_db, sync_forks
from utils import generate_random_string

app = Flask(__name__)


@app.route('/')
def home():
    forks = get_forks_from_db()
    return render_template('home.html', forks=forks)


@app.route('/update', methods=['POST'])
def update_fork():
    data = json.loads(request.get_data().decode('utf-8'))
    url = data.get('url')
    update_strategy = data.get('strategy')
    random_string = generate_random_string()
    args = [random_string, url, UPSTREAM_REPO_URL, 'WhiteJaeger', update_strategy]

    rc: CompletedProcess = run([os.path.join(CURRENT_DIR, 'update.sh'), *args], capture_output=True)

    stdout = rc.stdout.decode('utf-8')
    stderr = rc.stderr.decode('utf-8')

    result = {'returnCode': str(rc.returncode)}
    return json.dumps(result)


@app.route('/sync-forks', methods=['POST'])
def sync_forks_from_github():
    sync_forks()
    return json.dumps({'result': 'ok'})


if __name__ == '__main__':
    app.run()
