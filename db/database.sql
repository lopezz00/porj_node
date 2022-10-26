CREATE DATABASE IF NOT EXISTS companydb;

USE companydb;

CREATE TABLE employee (
  id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) DEFAULT NULL,
  salary INT(11) DEFAULT NULL, 
  PRIMARY KEY(id)
);

DESCRIBE employee;

INSERT INTO employee values (1, 'Ryan Ray', 1000),
                            (2, 'Joe McMillan', 20000),
                            (3, 'John Carter', 3500),
                            (4, 'Marc Lopez', 1500),
                            (5, 'Peter Parker', 9000);

-- SELECT * FROM employee;