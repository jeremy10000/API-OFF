CREATE DATABASE IF NOT EXISTS Pur_beurre_01072019JJ CHARACTER SET 'utf8';

USE Pur_beurre_01072019JJ;

CREATE TABLE IF NOT EXISTS Category(
id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
category VARCHAR(100) NOT NULL UNIQUE
)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Product(
id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
name VARCHAR(200) NOT NULL UNIQUE,
description TEXT NOT NULL,
category INT UNSIGNED NOT NULL,
store VARCHAR(150) NOT NULL,
url VARCHAR(500) NOT NULL,
nutrition_grade VARCHAR(1) NOT NULL
)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Save(
id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
id_product INT UNSIGNED NOT NULL,
id_new_product INT UNSIGNED NOT NULL
)
ENGINE = InnoDB;

ALTER TABLE Save
ADD CONSTRAINT fk_save_product_id
FOREIGN KEY (id_product) REFERENCES Product(id);

ALTER TABLE Save
ADD CONSTRAINT fk_save_new_product_id
FOREIGN KEY (id_new_product) REFERENCES Product(id);

ALTER TABLE Product
ADD CONSTRAINT fk_category
FOREIGN KEY (category) REFERENCES Category(id);

ALTER TABLE Save
ADD UNIQUE ind_nutriscore (id_product, id_new_product);