CREATE TABLE IF NOT EXISTS forks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    updateStatus TEXT NOT NULL,
    syncStatus TEXT NOT NULL,
    lastUpdateTime timestamp,
    lastSyncTime timestamp
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
