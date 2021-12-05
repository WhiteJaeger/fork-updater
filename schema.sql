DROP TABLE IF EXISTS forks;

CREATE TABLE forks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    updateStatus TEXT NOT NULL,
    syncStatus TEXT NOT NULL,
    lastUpdateTime timestamp,
    lastSyncTime timestamp
);
