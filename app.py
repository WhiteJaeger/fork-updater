from flask import Flask, render_template, request, json
from subprocess import run, CompletedProcess
from utils import get_forks
import os


app = Flask(__name__)
cur_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello_world():
    forks = get_forks()
    return render_template('home.html', names=list(forks.keys()), fork_urls=list(forks.values()))


@app.route('/update', methods=['POST'])
def update_fork():
    data = json.loads(request.get_data().decode('utf-8'))
    url = data.get('url')
    rc: CompletedProcess = run(os.path.join(cur_dir, 'test.sh'))
    return str(rc.returncode)


if __name__ == '__main__':
    app.run()
