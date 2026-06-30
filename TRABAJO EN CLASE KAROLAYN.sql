-- =========================================================
-- EJERCICIO: TRANSACCIONES SQL
-- TEMA: COMPRA DE BOLETOS PARA CONCIERTO DE BTS
-- =========================================================

-- Evita el error de Safe Update Mode en MySQL Workbench
SET SQL_SAFE_UPDATES = 0;

-- =========================================================
-- 1. CREAR BASE DE DATOS Y TABLAS
-- =========================================================

DROP DATABASE IF EXISTS concierto_bts;
CREATE DATABASE concierto_bts;
USE concierto_bts;

CREATE TABLE boletos (
    id_boleto INT PRIMARY KEY AUTO_INCREMENT,
    zona VARCHAR(50),
    precio DECIMAL(10,2),
    stock INT
) ENGINE=InnoDB;

CREATE TABLE compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    nombre_cliente VARCHAR(100),
    zona VARCHAR(50),
    cantidad INT,
    total DECIMAL(10,2),
    estado VARCHAR(50)
) ENGINE=InnoDB;

INSERT INTO boletos (zona, precio, stock) VALUES
('VIP', 250.00, 15),
('General', 120.00, 13),
('Preferencial', 180.00, 10);

-- Observamos los datos iniciales
SELECT * FROM boletos;
SELECT * FROM compras;


-- =========================================================
-- 2. EJERCICIO CON SAVEPOINT
-- =========================================================

START TRANSACTION;

-- Se observa el stock inicial de boletos VIP
SELECT * FROM boletos WHERE id_boleto = 1;

-- Se descuentan 2 boletos VIP
UPDATE boletos
SET stock = stock - 2
WHERE id_boleto = 1 AND stock >= 2;

-- Se observa que el stock bajó de 15 a 13
SELECT * FROM boletos WHERE id_boleto = 1;

-- Se guarda un punto de recuperación después del descuento
SAVEPOINT descuento_realizado;

-- Se registra la compra
INSERT INTO compras (nombre_cliente, zona, cantidad, total, estado)
VALUES ('Karolayn', 'VIP', 2, 500.00, 'Pendiente de pago');

-- Se observa que la compra fue registrada
SELECT * FROM compras;

-- Se simula un error en el pago y se vuelve al punto guardado
ROLLBACK TO descuento_realizado;

-- La compra desaparece, pero el stock queda descontado
SELECT * FROM compras;
SELECT * FROM boletos WHERE id_boleto = 1;

COMMIT;


-- =========================================================
-- 3. REINICIAR DATOS
-- =========================================================

TRUNCATE TABLE compras;

UPDATE boletos
SET stock = 15
WHERE id_boleto = 1;

UPDATE boletos
SET stock = 13
WHERE id_boleto = 2;

UPDATE boletos
SET stock = 10
WHERE id_boleto = 3;

SELECT * FROM boletos;
SELECT * FROM compras;


-- =========================================================
-- 4. EJERCICIO CON ROLLBACK FÍSICO
-- =========================================================

START TRANSACTION;

-- Se observa el stock inicial
SELECT * FROM boletos WHERE id_boleto = 1;

-- Se descuenta 1 boleto VIP
UPDATE boletos
SET stock = stock - 1
WHERE id_boleto = 1;

-- Se observa que el stock bajó de 15 a 14
SELECT * FROM boletos WHERE id_boleto = 1;

-- Se cancela toda la transacción
ROLLBACK;

-- El stock vuelve a 15
SELECT * FROM boletos WHERE id_boleto = 1;


-- =========================================================
-- 5. COMPENSACIÓN LÓGICA
-- =========================================================

TRUNCATE TABLE compras;

UPDATE boletos
SET stock = 15
WHERE id_boleto = 1;

START TRANSACTION;

-- Se descuenta un boleto VIP
UPDATE boletos
SET stock = stock - 1
WHERE id_boleto = 1;

-- Se registra la compra como aprobada
INSERT INTO compras (nombre_cliente, zona, cantidad, total, estado)
VALUES ('Karolayn', 'VIP', 1, 250.00, 'Aprobada');

COMMIT;

-- Se observa la compra aprobada y el stock descontado
SELECT * FROM boletos WHERE id_boleto = 1;
SELECT * FROM compras;

-- Ahora se simula que el pago falló después de confirmar la compra
UPDATE compras
SET estado = 'Cancelada por fallo de pago'
WHERE id_compra = 1;

-- Se devuelve el boleto al stock
UPDATE boletos
SET stock = stock + 1
WHERE id_boleto = 1;

-- Se observa que la compra no se borró, solo cambió de estado
SELECT * FROM boletos WHERE id_boleto = 1;
SELECT * FROM compras;


-- =========================================================
-- 6. REINICIAR DATOS ANTES DE TIMEOUT Y DEADLOCK
-- =========================================================

TRUNCATE TABLE compras;

UPDATE boletos
SET stock = 15
WHERE id_boleto = 1;

UPDATE boletos
SET stock = 13
WHERE id_boleto = 2;

UPDATE boletos
SET stock = 10
WHERE id_boleto = 3;

SELECT * FROM boletos;
SELECT * FROM compras;