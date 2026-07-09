# Simulación de Transacciones con Savepoints, Deadlocks y Timeouts

## Introducción

Este proyecto simula un sistema de reservas turísticas usando **Python** y **PostgreSQL**. El objetivo es comprender cómo funcionan las transacciones en una base de datos relacional, utilizando **savepoints**, manejo de errores, compensaciones, deadlocks y timeouts.

El escenario consiste en reservar tres servicios:

1. Vuelo.
2. Hotel.
3. Transporte.

La reserva solo debe completarse si los tres servicios tienen disponibilidad.



## Conceptos principales

### Transacciones y savepoints

Una transacción permite ejecutar varias operaciones como una sola unidad. Si todo sale bien, se confirma con `COMMIT`; si ocurre un error, se revierte con `ROLLBACK`.

Un `SAVEPOINT` es un punto intermedio dentro de una transacción. Permite regresar a una parte específica sin cancelar todo desde el inicio.

En este proyecto se usa un savepoint después de reservar el vuelo. Si el hotel no tiene cupo, el sistema vuelve a ese punto y cancela el vuelo mediante una compensación.

### Deadlock

Un deadlock ocurre cuando dos transacciones se bloquean mutuamente. Por ejemplo, una transacción bloquea primero vuelos y luego hoteles, mientras otra bloquea primero hoteles y luego vuelos.

Esto provoca que ambas se queden esperando. PostgreSQL detecta el problema y cancela una de las transacciones.

### Timeout

Un timeout ocurre cuando una operación tarda demasiado tiempo. La base de datos cancela la operación para evitar que el sistema quede bloqueado indefinidamente.


## Estructura del proyecto

```text
simulacion_transacciones.py
README.md
requirements.txt
.gitignore


### Archivos

* `simulacion_transacciones.py`: script principal de la simulación.
* `README.md`: documentación del proyecto.
* `requirements.txt`: dependencias necesarias.
* `.gitignore`: archivos que no se deben subir al repositorio.


## Instalación

Instalar la librería necesaria:

```bash
pip install psycopg2-binary


O instalar desde el archivo de dependencias:

```bash
pip install -r requirements.txt




## Funcionamiento del sistema

El programa crea tres tablas principales:

* `vuelos`: almacena vuelos y asientos disponibles.
* `hoteles`: almacena hoteles y habitaciones disponibles.
* `transportes`: almacena vehículos disponibles.

Luego inserta datos de prueba y ejecuta las simulaciones.



## Simulación de reserva

El flujo normal de la reserva es:

1. Se descuenta un asiento del vuelo.
2. Se crea un savepoint.
3. Se intenta reservar una habitación de hotel.
4. Se reserva un transporte.
5. Si todo sale bien, se confirma la transacción.

Si el hotel no tiene cupo:

1. Se vuelve al savepoint.
2. Se cancela la reserva del vuelo.
3. Se evita dejar datos incompletos.
4. Se finaliza la transacción de forma controlada.



## Simulación de deadlock

Para simular el deadlock se ejecutan dos transacciones al mismo tiempo:

* La primera actualiza vuelos y luego hoteles.
* La segunda actualiza hoteles y luego vuelos.

Como ambas intentan acceder a recursos bloqueados por la otra, se genera un deadlock. PostgreSQL detecta el bloqueo y cancela una de las transacciones para que la otra pueda continuar.



## Simulación de timeout

La simulación de timeout consiste en configurar un tiempo máximo de espera para una transacción. Luego se ejecuta una operación lenta. Si la operación supera el tiempo permitido, PostgreSQL la cancela y se realiza un rollback.



## Resultados obtenidos

### Reserva exitosa

Cuando hay disponibilidad en vuelo, hotel y transporte, la transacción se completa correctamente.

```text
Reserva de vuelo realizada.
Reserva de hotel realizada.
Reserva de transporte realizada.
Transacción confirmada correctamente.


### Hotel sin cupo

Cuando el hotel no tiene habitaciones disponibles, se usa el savepoint y se cancela el vuelo reservado.

```text
Vuelo reservado.
Hotel sin cupo.
Rollback al savepoint.
Compensación realizada: vuelo cancelado.
```

### Deadlock

Cuando dos transacciones bloquean recursos en orden contrario, PostgreSQL detecta el deadlock.

```text
Deadlock detectado.
Una transacción fue cancelada.
La otra transacción continuó correctamente.
```

### Timeout

Cuando una operación supera el tiempo máximo permitido, se cancela.

```text
Timeout alcanzado.
Operación cancelada.
Rollback ejecutado.
```

## Preguntas de reflexión

### 1. ¿Por qué es importante usar savepoints en transacciones largas? ¿Qué problema resuelven?

Los savepoints son importantes porque permiten volver a un punto específico dentro de una transacción sin cancelar todo el proceso. Resuelven el problema de tener que repetir una transacción completa cuando solo falló una parte.

### 2. ¿Qué pasaría si no usáramos savepoints y el hotel no tuviera cupo?

Si no se usaran savepoints, el sistema podría descontar el vuelo aunque el hotel no se haya reservado. Esto generaría una reserva incompleta y datos inconsistentes, porque el cliente tendría un vuelo apartado, pero no tendría hotel ni transporte.

### 3. ¿Cómo se produce un deadlock?

Un deadlock se produce cuando dos transacciones se bloquean entre sí. En el ejemplo, una transacción bloquea vuelos y luego intenta bloquear hoteles, mientras otra bloquea hoteles y luego intenta bloquear vuelos. PostgreSQL detecta el problema y cancela una de ellas.

### 4. ¿Qué estrategias existen para evitar deadlocks?

Algunas estrategias son:

* Acceder a las tablas siempre en el mismo orden.
* Mantener las transacciones lo más cortas posible.
* Usar bloqueos solo cuando sean necesarios.
* Manejar errores con rollback.
* Implementar reintentos automáticos cuando una transacción falla.

### 5. ¿Qué sucede cuando una transacción alcanza el timeout?

Cuando una transacción alcanza el timeout, la base de datos cancela la operación. Esto evita que el sistema quede bloqueado por demasiado tiempo. Para el usuario final, puede aparecer un mensaje de error o de espera agotada. Para manejarlo, se pueden usar mensajes claros, rollback automático y reintentos controlados.



## Conclusión

Con esta práctica se comprendió la importancia de manejar correctamente las transacciones en una base de datos. Los savepoints permiten controlar errores parciales, los deadlocks muestran los riesgos de la concurrencia y los timeouts ayudan a evitar esperas prolongadas.

Este tipo de simulación es útil para entender cómo mantener la consistencia de los datos en sistemas reales, especialmente cuando varias operaciones dependen unas de otras.
