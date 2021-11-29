from flask import g
import os
from constants import CURRENT_DIR
from utils import get_forks
from typing import Optional, Dict
import sqlite3


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(os.path.join(CURRENT_DIR, 'database.db'))
    db.row_factory = sqlite3.Row

    return db


def get_forks_from_db() -> Dict[str, str]:
    db = get_db()
    forks_from_db = db.execute('SELECT * FROM forks').fetchall()
    forks = {}
    for fork in forks_from_db:
        forks[fork['name']] = fork['url']
    db.close()
    return forks


def get_fork_by_url(url: str) -> Optional[sqlite3.Row]:
    db = get_db()
    fork = db.execute("SELECT * FROM forks WHERE url = ?", (url,)).fetchone()
    db.close()
    return fork


def add_fork(name: str, url: str, status: str):
    if get_fork_by_url(url):
        return
    db = get_db()
    db.execute("INSERT INTO forks (name, url, status) VALUES (?, ?, ?)",
               (name, url, status)
               )
    db.commit()
    db.close()


def sync_forks():
    fetched_forks = get_forks()
    db = get_db()
    for fork_name, fork_url in fetched_forks.items():
        fork = db.execute("SELECT * FROM forks WHERE url = ?", (fork_url,)).fetchone()
        if fork:
            continue
        db.execute("INSERT INTO forks (name, url, status) VALUES (?, ?, ?)",
                   (fork_name, fork_url, 'recently added')
                   )
    db.commit()
    db.close()
