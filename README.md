# Fork Updater App

This app provides an interface to interact with forks of the given upstream.

## Run locally

1. Pre-requisites:
   1. OS: Unix* with `bash` as `.sh` scripts are used to interact with `git`.
2. Create virtual environment;
3. Install dependencies:
   1. `python -m pip install -r requirements.txt`
4. Init database:
   1. `python init_db.py`
   2. You should see the `database.db` file in the root directory.
5. Set environment variables:
   1. `export FLASK_APP=app.py`
   2. `export AUTH_TOKEN=${AUTH_TOKEN}` - the GitHub Personal Access Token with access to the forks.
   3. `export FLASK_DEBUG=1` - can be omitted if you require production mode.
   4. `export FLASK_ENV=development` - can be omitted if you require production mode.
6. Run the app:
   1. `python -m flask run`
7. Navigate to the `localhost:5000` in your browser.
