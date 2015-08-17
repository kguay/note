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
INSERT INTO "users" VALUES(1,'jbrown',3,'jbrown@bigelow.org','pbkdf2:sha1:1000$HH8MSVNJ$b2c6e5531c4da82ec004c00103785f0f1b7b9d0a',NULL,'Joe Brown');
INSERT INTO "users" VALUES(2,'fsmith',2,'fsmith@bigelow.org','pbkdf2:sha1:1000$I813cP6H$249e0bbdffffb5ac580955aa2cd8c16bc418d92f',NULL,'Frank Smith');

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

INSERT INTO "expenses" VALUES(1,1,'Joe Brown','2014-08-25 12:22:35','08/25/2014','08/16/2014','Aquaprep Filters (600 pk x 10)','VWR','29.95',438853,'/receipts/jbrown/jbrown_1.pdf',0);
INSERT INTO "expenses" VALUES(2,1,'Joe Brown','2015-01-21 14:12:02','01/21/2015','01/13/2015','UPS Backup','Amazon','175.26',386933,'/receipts/jbrown/jbrown_2.pdf',0);
INSERT INTO "expenses" VALUES(3,1,'Joe Brown','2015-03-05 10:23:24','03/05/2015','02/30/2015','Disposable gloves for lab','VWR','32.19',582333,'/receipts/jbrown/jbrown_3.pdf',0);
INSERT INTO "expenses" VALUES(4,1,'Joe Brown','2015-04-25 10:43:27','04/25/2015','04/23/2015','Lab supplies:
- paper towels
- windex','Hannaford',17.85,353343,'/receipts/jbrown/jbrown_4.pdf',0);
INSERT INTO "expenses" VALUES(5,2,'Frank Smith','2015-01-12 10:43:27','01/12/2015','01/10/2015','Lab Supplies (pens and baggies)','Hannaford','10.90',334223,'/receipts/fsmith/fsmith_5.pdf',0);
INSERT INTO "expenses" VALUES(6,2,'Frank Smith','2015-05-29 10:43:27','05/29/2015','05/27/2015','Totes for July cruise','Amazon','88.30',394334,'/receipts/fsmith/fsmith_6.pdf',0);
INSERT INTO "expenses" VALUES(7,1,'Joe Brown','2015-06-14 10:43:27','06/14/2015','06/13/2015','Kim wipes','Amazon','112.48',342223,'/receipts/jbrown/jbrown_7.pdf',0);

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
