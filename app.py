from flask import Flask, render_template
from subprocess import run, CompletedProcess
from utils import get_forks

app = Flask(__name__)


@app.route('/')
def hello_world():
    forks = get_forks()
    return render_template('home.html', names=list(forks.keys()), fork_urls=list(forks.values()))


if __name__ == '__main__':
    app.run()
