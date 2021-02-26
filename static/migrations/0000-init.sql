CREATE TABLE IF NOT EXISTS Guilds (
    id              BIGINT NOT NULL PRIMARY KEY,
    prefix          VARCHAR(255) NOT NULL DEFAULT '>',
    config          TEXT NOT NULL DEFAULT '{}',
    banned          BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Users (
    id              BIGINT NOT NULL PRIMARY KEY,
    banned          BOOLEAN NOT NULL DEFAULT FALSE,
    config          TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS Cases (
    id              BIGINT NOT NULL PRIMARY KEY,
    guildid         BIGINT NOT NULL,
    userid          BIGINT NOT NULL,
    modid           BIGINT NOT NULL,
    username        VARCHAR(255) NOT NULL,
    modname         VARCHAR(255) NOT NULL,
    case_type       VARCHAR(255) NOT NULL,
    case_data       TEXT NOT NULL,
    case_hidden     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMP DEFAULT NULL,
    expired         BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Reminders (
    id              BIGINT NOT NULL PRIMARY KEY,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMP NOT NULL,
    userid          BIGINT NOT NULL,
    message_link    VARCHAR(255) NOT NULL,
    expired         BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS Tags (
    name            VARCHAR(256) NOT NULL,
    guildid         BIGINT NOT NULL,
    content         TEXT,
    PRIMARY KEY (name, guildid)
);

CREATE TABLE IF NOT EXISTS Todos (
    id              BIGINT NOT NULL PRIMARY KEY ,
    userid          BIGINT NOT NULL,
    content         TEXT NOT NULL,
    completed       BOOLEAN DEFAULT FALSE
);
