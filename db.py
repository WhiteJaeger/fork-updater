import os
import sqlite3
from typing import Optional, Dict

from flask import g

from constants import CURRENT_DIR, GeneralStatusMessages
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

    db.close()
    return forks


def get_fork_by_url(url: str) -> Optional[sqlite3.Row]:
    db = get_db()
    fork = db.execute("SELECT * FROM forks WHERE url = ?", (url,)).fetchone()
    db.close()
    return fork


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
    db.close()
