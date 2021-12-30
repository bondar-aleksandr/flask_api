CREATE TABLE if not exists "user" (
	"id"	INTEGER UNIQUE,
	"login"	TEXT UNIQUE,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);