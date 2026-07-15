# Simulación de Transacciones en PostgreSQL

## Introducción teórica

### Transacciones y Savepoints

Una transacción en una base de datos permite agrupar varias operaciones SQL dentro de un mismo proceso. Estas operaciones pueden confirmarse mediante un `COMMIT` cuando todo funciona correctamente o cancelarse utilizando `ROLLBACK` si se presenta algún error.

Los `SAVEPOINT` permiten crear puntos de control dentro de una transacción. Gracias a ellos, es posible regresar a una etapa específica del proceso sin cancelar inmediatamente todas las operaciones realizadas.

Este mecanismo resulta útil en sistemas que realizan varios pasos consecutivos, ya que permite controlar errores parciales y mantener la consistencia de la información almacenada.

### Deadlocks

Un deadlock o interbloqueo ocurre cuando dos transacciones mantienen recursos bloqueados y cada una intenta acceder al recurso que está siendo utilizado por la otra.

Como consecuencia, ambas operaciones quedan esperando mutuamente y no pueden continuar normalmente.

Este problema puede aparecer en sistemas donde varios usuarios realizan operaciones al mismo tiempo, como una plataforma de compra de boletos para conciertos.

PostgreSQL puede detectar automáticamente un deadlock y cancelar una de las transacciones involucradas para liberar los recursos bloqueados.

### Timeouts

Los timeouts permiten establecer un tiempo máximo de ejecución para una operación en PostgreSQL.

Cuando una consulta supera el tiempo configurado, el sistema cancela automáticamente su ejecución.

Esto permite evitar que consultas demasiado lentas o procesos bloqueados permanezcan activos durante mucho tiempo y afecten el rendimiento de la base de datos.

## Escenario del sistema

En esta práctica se desarrolla una simulación de compra de boletos para un concierto de BTS.

El sistema realiza tres operaciones principales:

* Verificación y descuento de boletos disponibles para el concierto.
* Selección y reserva de un asiento.
* Validación del proceso de pago.

### Regla del sistema

Si el asiento seleccionado no se encuentra disponible, el sistema realiza las siguientes acciones:

1. Regresa al savepoint creado después de descontar el boleto.
2. Devuelve el boleto al inventario disponible.
3. Cancela el proceso de compra.

Este comportamiento representa una situación que puede ocurrir en una plataforma real de venta de entradas.

El objetivo es evitar que un boleto quede descontado cuando el usuario no logró completar correctamente la selección del asiento o el proceso de compra.

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

Ejecutar los siguientes comandos desde una terminal:

```bash
git clone https://github.com/Karolayn8756/TRABAJO-EN-CLASE-.git
cd TRABAJO-EN-CLASE-
```

### 2. Instalar dependencias

Para conectar Python con PostgreSQL se utiliza la biblioteca `psycopg2`.

Ejecutar:

```bash
pip install psycopg2-binary
```

### 3. Configurar la base de datos en PostgreSQL

Antes de ejecutar el proyecto se debe comprobar que la base de datos esté creada correctamente.

Datos utilizados para la conexión:

* Base de datos: `boletos_bts`
* Usuario: `emilia`
* Contraseña: `root`
* Host: `localhost`
* Puerto: `5432`

Estos datos deben coincidir con la configuración utilizada dentro del código Python.

```python
def nueva_conexion():
    return psycopg2.connect(
        database="boletos_bts",
        user="emilia",
        password="root",
        host="localhost",
        port="5432"
    )
```

### 4. Ejecutar el programa

Desde la carpeta del proyecto ejecutar:

```bash
python main.py
```

### 5. Verificar los resultados

El funcionamiento del programa puede comprobarse mediante la consola y pgAdmin.

En la consola se pueden observar los siguientes procesos:

* Inicio de la compra.
* Verificación de boletos disponibles.
* Creación de savepoints.
* Reserva del asiento.
* Procesamiento del pago.
* Confirmación de la compra.
* Rollbacks.
* Deadlocks.
* Timeouts.

Desde pgAdmin se pueden consultar los cambios realizados en las tablas:

* `conciertos`
* `asientos`
* `pagos`

## Explicación del código

### Conexión a PostgreSQL

La conexión con PostgreSQL se realiza mediante la biblioteca `psycopg2`.

La función `nueva_conexion()` contiene los parámetros necesarios para conectarse con la base de datos.

```python
def nueva_conexion():
    return psycopg2.connect(
        database="boletos_bts",
        user="emilia",
        password="root",
        host="localhost",
        port="5432"
    )
```

Cada proceso obtiene una conexión con PostgreSQL.

El control manual de las transacciones permite utilizar `commit()` para guardar los cambios y `rollback()` para cancelar las operaciones cuando ocurre un problema.

## Flujo de la transacción

El sistema de compra sigue el siguiente proceso:

```text
BEGIN
Verificar boletos disponibles
Descontar boleto
SAVEPOINT sp_boleto
Verificar asiento
Reservar asiento
SAVEPOINT sp_asiento
Validar pago
Confirmar compra
COMMIT
```

Primero se verifica la cantidad de boletos disponibles para el concierto.

Cuando existe disponibilidad, se descuenta un boleto y se crea el primer savepoint:

```sql
SAVEPOINT sp_boleto;
```

Después se consulta el estado del asiento seleccionado.

Si el asiento está disponible, su estado cambia y se crea un segundo savepoint:

```sql
SAVEPOINT sp_asiento;
```

Finalmente, el sistema procesa y valida el pago.

Si las operaciones se completan correctamente, se utiliza:

```python
conn.commit()
```

El `COMMIT` permite guardar permanentemente todos los cambios realizados dentro de la transacción.

## Manejo de errores

El programa contiene diferentes validaciones durante la compra.

Si no existen boletos disponibles, se genera una excepción y la operación es cancelada.

Cuando el asiento seleccionado no está disponible, el sistema utiliza:

```sql
ROLLBACK TO SAVEPOINT sp_boleto;
```

Después se incrementa nuevamente la cantidad de boletos disponibles para devolver el boleto que había sido descontado.

Si ocurre un error general durante la ejecución del programa, se utiliza:

```python
conn.rollback()
```

Esta instrucción cancela las operaciones pendientes de la transacción.

El manejo de errores evita situaciones incorrectas, como descontar un boleto cuando la compra realmente no pudo completarse.

## Simulación de Deadlock

Para demostrar un deadlock se ejecutan dos transacciones concurrentes utilizando hilos de Python.

La primera transacción ejecuta el siguiente proceso:

```text
T1 bloquea conciertos
T1 espera
T1 intenta bloquear asientos
```

La segunda transacción realiza las operaciones en un orden diferente:

```text
T2 bloquea asientos
T2 espera
T2 intenta bloquear conciertos
```

El problema ocurre porque la primera transacción mantiene bloqueado el concierto mientras espera acceder al asiento.

Al mismo tiempo, la segunda transacción mantiene bloqueado el asiento mientras espera acceder al concierto.

La situación puede representarse de la siguiente manera:

```text
T1 tiene CONCIERTO y espera ASIENTO
T2 tiene ASIENTO y espera CONCIERTO
```

Esto genera una espera circular entre las dos transacciones.

PostgreSQL detecta automáticamente el deadlock y cancela una de las transacciones para liberar los recursos bloqueados.

La transacción cancelada realiza un rollback y la otra puede continuar con su ejecución.

## Simulación de Timeout

Para realizar la simulación de timeout se configura el siguiente límite:

```sql
SET statement_timeout = '3000';
```

El valor `3000` representa un máximo de 3000 milisegundos o 3 segundos.

Posteriormente se ejecuta:

```sql
SELECT pg_sleep(6);
```

La función `pg_sleep(6)` intenta mantener la consulta activa durante 6 segundos.

Como el tiempo permitido es únicamente de 3 segundos, PostgreSQL cancela automáticamente la operación.

El error generado es capturado por Python y se realiza un rollback de la transacción.

El timeout ayuda a evitar que procesos demasiado lentos permanezcan activos durante largos periodos y afecten a otros usuarios del sistema.

## Preguntas de reflexión

### 1. ¿Por qué es importante utilizar savepoints en transacciones extensas?

Los savepoints permiten establecer puntos de control dentro de una transacción.

Si ocurre un problema durante una operación, es posible regresar a una etapa específica sin cancelar inmediatamente todo el proceso.

En el sistema de boletos, permiten controlar errores relacionados con la selección del asiento y las diferentes etapas de la compra.

### 2. ¿Qué ocurriría si no se utilizaran savepoints y el asiento ya estuviera ocupado?

Sin savepoints sería necesario cancelar completamente la transacción o implementar otras operaciones para controlar manualmente los cambios realizados.

Por ejemplo, el sistema podría haber descontado un boleto antes de detectar que el asiento seleccionado estaba ocupado.

Los savepoints facilitan el control de estas situaciones y permiten mantener los datos en un estado consistente.

### 3. ¿Cómo se produce un deadlock y cómo se representa en el programa?

Un deadlock ocurre cuando dos transacciones esperan recursos que se encuentran bloqueados mutuamente.

En el programa, la primera transacción bloquea el concierto y posteriormente intenta acceder al asiento.

La segunda transacción realiza el proceso contrario, bloqueando primero el asiento e intentando después acceder al concierto.

Debido al orden inverso de acceso a los recursos, se produce una espera circular.

PostgreSQL identifica automáticamente el deadlock y cancela una de las transacciones involucradas.

### 4. ¿Qué estrategias se pueden utilizar para disminuir los deadlocks?

Algunas estrategias para reducir la aparición de deadlocks son:

* Acceder a las tablas y registros siguiendo siempre el mismo orden.
* Mantener las transacciones cortas.
* Evitar bloqueos que no sean necesarios.
* Utilizar índices adecuados.
* Optimizar las consultas SQL.
* Implementar reintentos automáticos cuando se detecte un deadlock.

Una de las principales medidas consiste en mantener un orden consistente al acceder a los recursos.

### 5. ¿Qué ocurre cuando una transacción alcanza el timeout?

Cuando una operación supera el tiempo máximo configurado, PostgreSQL cancela automáticamente su ejecución.

Para el usuario, esto puede significar que la compra del boleto no se completó correctamente.

En un sistema real se podrían implementar diferentes mecanismos para manejar este problema:

* Mostrar mensajes de error claros.
* Solicitar al usuario que vuelva a intentar la compra.
* Implementar reintentos automáticos.
* Optimizar las consultas.
* Revisar el rendimiento de la base de datos.
* Configurar tiempos de espera adecuados.

El timeout permite proteger la base de datos frente a operaciones demasiado lentas.

## Conclusión

Esta práctica permitió comprender el funcionamiento de las transacciones en PostgreSQL mediante la simulación de un sistema de compra de boletos para un concierto de BTS.

Durante el desarrollo se utilizaron savepoints para crear puntos de control dentro del proceso de compra y permitir el manejo de errores parciales.

También se realizó una simulación de deadlock utilizando dos transacciones concurrentes que acceden al concierto y al asiento en un orden diferente.

Finalmente, se implementó `statement_timeout` para demostrar cómo PostgreSQL puede cancelar consultas que superan un tiempo máximo de ejecución.

Estos mecanismos son importantes en sistemas de venta de boletos donde varios usuarios pueden intentar realizar compras simultáneamente. El manejo adecuado de las transacciones permite conservar la consistencia de los datos, controlar problemas de concurrencia y mantener un funcionamiento estable de la base de datos.

## Evidencias

### Imagen 1: Compra exitosa y creación de SAVEPOINT
<img width="720" height="282" alt="{367B9642-4E2E-4762-9FC9-DB9DAD7406E9}" src="https://github.com/user-attachments/assets/87fafc37-d378-4c25-9ff7-96a41d697132" />

### Imagen 2: Simulación de Deadlock

<img width="957" height="253" alt="{3D5E5925-1B07-4A92-822B-8A1880566C84}" src="https://github.com/user-attachments/assets/de5b68d8-8003-421f-9a18-c218fc6f7046" />


### Imagen 3: Simulación de Timeout

<img width="963" height="135" alt="{4E25D906-235C-4BD3-848A-C93104EE7203}" src="https://github.com/user-attachments/assets/aeae8261-ace7-4155-9d6b-a71e20fa804d" />


### Imagen 4: Ejecución completa del programa


### Imagen 5: Base de datos creada

<img width="816" height="538" alt="{C9081E57-16DB-4A4B-88D4-C29D24979FE7}" src="https://github.com/user-attachments/assets/ebc0fcd5-eb45-419a-9cbf-9327ab46a79f" />

<img width="778" height="549" alt="{6F5E5A93-DF3A-429F-8C09-70D4BD8C4F0B}" src="https://github.com/user-attachments/assets/c3f083b7-5666-4dee-8376-624125426310" />
<img width="652" height="565" alt="{B91ADC89-FDB5-4586-8B4B-BC757A422BB0}" src="https://github.com/user-attachments/assets/a45c568b-0172-4521-ba72-17a3f52e2417" />
<img width="859" height="331" alt="{B7F01F99-2FAE-43A7-9EC0-C5EF57E03EBB}" src="https://github.com/user-attachments/assets/20b30147-fa08-4c25-bece-bc8bcdc71d5c" />
