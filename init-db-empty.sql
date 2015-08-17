PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE roles (
id INTEGER NOT NULL, 
name VARCHAR(64), "default" BOOLEAN, permissions INTEGER, 
PRIMARY KEY (id), 
UNIQUE (name)
);
INSERT INTO "roles" VALUES(1,'Moderator',0,15);
INSERT INTO "roles" VALUES(2,'Administrator',0,255);
INSERT INTO "roles" VALUES(3,'User',1,7);

CREATE TABLE users (
id INTEGER NOT NULL, 
username VARCHAR(64), 
role_id INTEGER, email VARCHAR(64), password_hash VARCHAR(128), confirmed BOOLEAN, full_name text, 
PRIMARY KEY (id), 
FOREIGN KEY(role_id) REFERENCES roles (id)
);

CREATE TABLE expenses (
id INTEGER NOT NULL, 
user_id INTEGER,
username TEXT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
submit_date TEXT,
purchase_date TEXT,
description TEXT,
vendor TEXT, 
amount TEXT,
account INTEGER,
receipt TEXT,
approved INTEGER, 
PRIMARY KEY (id), 
FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE vendors (
id INTEGER NOT NULL, 
name VARCHAR(64),
url VARCHAR(128),
address VARCHAR(128),
phone VARCHAR(64),
PRIMARY KEY (id),
UNIQUE (name)
);
INSERT INTO "vendors" VALUES(1,'Amazon',NULL,NULL,NULL);
INSERT INTO "vendors" VALUES(2,'VWR',NULL,NULL,NULL);
INSERT INTO "vendors" VALUES(3,'Hannaford',NULL,NULL,NULL);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_roles_default ON roles ("default");
COMMIT;
