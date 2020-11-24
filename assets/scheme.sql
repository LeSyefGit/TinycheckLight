CREATE TABLE "iocs" (
	"id"	INTEGER UNIQUE,
	"value"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"tlp"	TEXT NOT NULL,
	"tag"	TEXT NOT NULL,
	"source"	TEXT NOT NULL,
	"added_on"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "whitelist" (
	"id"	INTEGER UNIQUE,
	"element"	TEXT NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"source"	TEXT NOT NULL,
	"added_on"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
