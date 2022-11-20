CREATE TABLE USUARI (
    email VARCHAR(30) NOT NULL PRIMARY KEY,
    nom VARCHAR(30) NOT NULL,
    cognom1 VARCHAR(30) NOT NULL,
    cognom2 VARCHAR(30),
    pw_hash VARCHAR(32) NOT NULL,               -- Contindrà el hash de la contrasenya de l'usuari. No salt. Sha(256) s'espera.
    rol VARCHAR(30) NOT NULL,
    id VARCHAR(8) NOT NULL,                     -- Valor targta RFID
    PRIMARY key (email)
);

CREATE TABLE MAQUINA (
    id_maquina INTEGER NOT NULL,
    id_lab INTEGER,
    nom_maquina VARCHAR(30) NOT NULL,
    descripcio VARCHAR(120),
    estat INTEGER NOT NULL,                     --2 apagada, 3 encesa, 4 fora de servei
    email VARCHAR(30) NOT NULL,
    calibracio REAL,
    PRIMARY KEY (id_maquina),
    FOREIGN KEY (id_lab) REFERENCES TECHLAB(id_techlab) ON DELETE CASCADE
);

CREATE TABLE TECHLAB (
    id_techlab INTEGER,
    aforament_max INTEGER NOT NULL,             -- Numero de maquines maximes que hi poiden haver al lab
    aforament_actual INTEGER NOT NULL,          -- Numero de mauqines existents al lab actualment
    maquines_numero INTEGER NOT NULL,           -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    maquines_ocupades INTEGER NOT NULL,         -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    PRIMARY key (id_techlab)
);

CREATE TABLE RESERVES (
    email VARCHAR(30) NOT NULL,
    id_maquina INTEGER NOT NULL,
    hora_entrada DATE NOT NULL,
    hora_sortida DATE NOT NULL,
    data DATE NOT NULL,
    reserva_feta INT NOT NULL,                  -- 0 RESERVA SENSE ENCARA USUARI, 1 RESERVA AMB USUARI, 2 HA ACABAT LA RESERVA
    PRIMARY KEY (email, id_maquina, hora_entrada, data),
    FOREIGN KEY (email) REFERENCES USUARI(email) ON DELETE CASCADE,
    FOREIGN KEY (id_maquina) REFERENCES MAQUINA(id_maquina) ON DELETE CASCADE
);

CREATE TABLE HISTORIAL(
    id INTEGER AUTO_INCREMENT,
    id_maquina INTEGER NOT NULL,
    email VARCHAR(30) NOT NULL,
    hora_entrada DATE NOT NULL,
    hora_sortida DATE NOT NULL,
    hora_consum DATE NOT NULL,                  -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi ja que volem el consum total i no per hores
    data DATE NOT NULL,
    consum INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_maquina) REFERENCES MAQUINA(id_maquina) ON DELETE CASCADE,
    FOREIGN KEY (email) REFERENCES USUARI(email) ON DELETE CASCADE
);

CREATE TABLE CONFIGMAQUINES(                    -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    nom_maquina VARCHAR(30) NOT NULL,           -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    ssid_wifi VARCHAR(30) NOT NULL,             -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    pswd_wifi VARCHAR(30) NOT NULL,             -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
    PRIMARY KEY (nom_maquina)                   -- Diria que no ho farem servir, ja ho eliminarem de la bd en el cas de que sigui aixi
);




-- CREATE DATABASE IF NOT EXISTS companydb;

-- USE companydb;

-- CREATE TABLE employee (
--   id INT(11) NOT NULL AUTO_INCREMENT,
--   name VARVARCHAR(45) DEFAULT NULL,
--   salary INT(11) DEFAULT NULL, 
--   PRIMARY KEY(id)
-- );

-- DESCRIBE employee;

-- INSERT INTO employee values (1, 'Ryan Ray', 1000),
--                             (2, 'Joe McMillan', 20000),
--                             (3, 'John Carter', 3500),
--                             (4, 'Marc Lopez', 1500),
--                             (5, 'Peter Parker', 9000);

-- SELECT * FROM employee;

-- INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES
--     ('upctech.solutions@gmail.com','Marc','Lopez','Arevalo','1234', 'Administrador',"c6888a9b");