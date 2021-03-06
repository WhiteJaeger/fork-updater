import os
import sqlite3
from typing import Optional, Dict

from flask import g
from werkzeug.security import generate_password_hash

from constants import CURRENT_DIR, GeneralStatusMessages
from models import User
from utils import get_forks_from_github


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(os.path.join(CURRENT_DIR, 'database.db'))
    db.row_factory = sqlite3.Row

    return db


def get_forks_from_db() -> Dict[str, Dict[str, str]]:
    db = get_db()
    forks_from_db = db.execute('SELECT * FROM forks').fetchall()
    forks = {}
    for fork in forks_from_db:
        update_time = fork['lastUpdateTime'] if fork['lastUpdateTime'] else str(GeneralStatusMessages.not_updated_yet)
        sync_time = fork['lastSyncTime'] if fork['lastSyncTime'] else str(GeneralStatusMessages.not_synced_yet)
        forks[fork['name']] = {'url': fork['url'],
                               'updateStatus': fork['updateStatus'],
                               'syncStatus': fork['syncStatus'],
                               'updateTime': update_time,
                               'syncTime': sync_time}

    db.commit()
    return forks


def sync_forks_list_with_github():
    fetched_forks = get_forks_from_github()
    db = get_db()
    for fork_name, fork_url in fetched_forks.items():
        fork = db.execute("SELECT * FROM forks WHERE url = ?", (fork_url,)).fetchone()
        if fork:
            continue
        db.execute("INSERT INTO forks (name, url, syncStatus, updateStatus) VALUES (?, ?, ?, ?)",
                   (fork_name,
                    fork_url,
                    str(GeneralStatusMessages.recently_added),
                    str(GeneralStatusMessages.recently_added))
                   )
    db.commit()


def add_user(email: str, password: str):
    db = get_db()
    db.execute("INSERT OR REPLACE INTO users (email, password) VALUES (?, ?)", (email, generate_password_hash(password)))
    db.commit()


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    db.commit()
    return user


def get_user_by_id(user_id: int) -> Optional[User]:
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.commit()
    if user:
        return User(user['id'], user['email'], user['password'])
    else:
        return None


def configure_admin_user(email: str, password: str):
    if not get_user_by_email(email):
        add_user(email, password)
