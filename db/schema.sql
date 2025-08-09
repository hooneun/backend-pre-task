BEGIN;
--
-- Create model Label
--
CREATE TABLE "contract_label"
(
    "id"         integer     NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name"       varchar(50) NOT NULL UNIQUE,
    "color"      varchar(7)  NOT NULL,
    "created_at" datetime    NOT NULL,
    "updated_at" datetime    NOT NULL
);
--
-- Create model Contact
--
CREATE TABLE "contracts_contact"
(
    "id"          integer      NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name"        varchar(100) NOT NULL,
    "email"       varchar(254) NULL,
    "phone"       varchar(20) NULL,
    "company"     varchar(100) NULL,
    "position"    varchar(50) NULL,
    "memo"        text NULL,
    "profile_url" varchar(200) NULL,
    "address"     varchar(200) NULL,
    "birthday"    date NULL,
    "website"     varchar(200) NULL,
    "created_at"  datetime     NOT NULL,
    "updated_at"  datetime     NOT NULL
);
CREATE TABLE "contracts_contact_labels"
(
    "id"         integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "contact_id" bigint  NOT NULL REFERENCES "contracts_contact" ("id") DEFERRABLE INITIALLY DEFERRED,
    "label_id"   bigint  NOT NULL REFERENCES "contract_label" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "idx_contact_name" ON "contracts_contact" ("name");
CREATE INDEX "idx_contact_email" ON "contracts_contact" ("email");
CREATE INDEX "idx_contact_phone" ON "contracts_contact" ("phone");
CREATE INDEX "idx_contact_created_at" ON "contracts_contact" ("created_at");
CREATE UNIQUE INDEX "contracts_contact_labels_contact_id_label_id_475275fd_uniq" ON "contracts_contact_labels" ("contact_id", "label_id");
CREATE INDEX "contracts_contact_labels_contact_id_4c312984" ON "contracts_contact_labels" ("contact_id");
CREATE INDEX "contracts_contact_labels_label_id_5ff2c0b8" ON "contracts_contact_labels" ("label_id");
COMMIT;