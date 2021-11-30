DROP TABLE IF EXISTS forks;

CREATE TABLE forks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    lastUpdateTime timestamp
);
