
CREATE TABLE IF NOT EXISTS family(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS genus(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    family_id INT(8),
    FOREIGN KEY(family_id) REFERENCES family(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS supplier(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    phone INT(11),
    address VARCHAR(40),
    email VARCHAR(40)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS category(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS product(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    amount INT(8),
    memo VARCHAR(40),
    family_id INT(8),
    genus_id INT(8),
    supplier_id INT(8),
    category_id INT(8),
    product_num VARCHAR(20),
    stock_status ENUM("", ""),
    FOREIGN KEY(family_id) REFERENCES family(id),
    FOREIGN KEY(genus_id)  REFERENCES genus(id),
    FOREIGN KEY(supplier_id) REFERENCES supplier(id),
    FOREIGN KEY(category_id) REFERENCES category(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS suppliercategory(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    category_id INT(8),
    supplier_id INT(8),
    FOREIGN KEY(supplier_id) REFERENCES supplier(id),
    FOREIGN KEY(category_id) REFERENCES category(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS sold(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    amount INT(8),
    revenue INT(8),
    distribute ENUM("shapee", "retail"),
    salesdate DATE,
    product_id INT(8),
    FOREIGN KEY(product_id) REFERENCES product(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS purchase(
    id INT(8) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    amount INT(8),
    expenses INT(8),
    stockdate DATE,
    product_id INT(8),
    FOREIGN KEY(product_id) REFERENCES product(id),
    category_id INT(8),
    supplier_id INT(8),
    FOREIGN KEY(supplier_id) REFERENCES supplier(id),
    FOREIGN KEY(category_id) REFERENCES category(id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;