CREATE DATABASE db_telegrambot;

\c db_telegrambot;

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE cars (
    id INTEGER PRIMARY KEY,
    owner_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    data JSONB NOT NULL
);

CREATE TABLE belongings (
    id INTEGER PRIMARY KEY,
    owner_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    data JSONB NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    receiver_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    data JSONB NOT NULL
);
