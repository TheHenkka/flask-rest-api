PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS countries;

CREATE TABLE item (
    item_id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
    item_name      VARCHAR(128) NOT NULL,
    item_price     INTEGER NOT NULL
);

INSERT INTO "item" VALUES(1,"item1",9.99);
INSERT INTO "item" VALUES(2,"item2",0);
INSERT INTO "item" VALUES(3,"item3",14);
INSERT INTO "item" VALUES(4,"item4",49);
INSERT INTO "item" VALUES(5,"item5",1);

CREATE TABLE cart (
    id              INTEGER  NOT NULL PRIMARY KEY  AUTOINCREMENT,
    items           VARCHAR  DEFAULT '[]',
    country         VARCHAR(128)
);

INSERT INTO "cart" VALUES(1,'[1,2,3]', 'Finland');
INSERT INTO "cart" VALUES(2,'[1,2,3,4,5]', 'Germany');
INSERT INTO "cart" VALUES(3,'[0]', 'Sweden');
INSERT INTO "cart" VALUES(4,'[1,1,3,4,4,5]', 'USA');
INSERT INTO "cart" VALUES(5,'[1,1,3,4,4,5]', 'Finland');

CREATE TABLE cart_items (
    cart_id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
    item_name      VARCHAR(128) NOT NULL,
    item_price     INTEGER NOT NULL
);

CREATE TABLE countries (
    id               INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
    country_name     VARCHAR(128)  UNIQUE
);

COMMIT;