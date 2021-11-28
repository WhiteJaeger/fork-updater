from flask import Flask, render_template, request, json
from subprocess import run, CompletedProcess
from utils import get_forks, generate_random_string
from constants import UPSTREAM_REPO_URL
import os


app = Flask(__name__)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello_world():
    forks = get_forks()
    return render_template('home.html', names=list(forks.keys()), fork_urls=list(forks.values()))


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


if __name__ == '__main__':
    app.run()
