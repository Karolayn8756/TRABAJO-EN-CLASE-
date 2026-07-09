# Simulación de Transacciones con Savepoints, Deadlocks y Timeouts

## Introducción

Este proyecto simula un sistema de venta de boletos para un concierto de BTS usando una base de datos relacional. El objetivo es comprender cómo funcionan las transacciones, los savepoints, los deadlocks y los timeouts cuando varias operaciones dependen entre sí.

En este caso, el sistema permite realizar una compra de boletos, verificar disponibilidad y controlar errores para evitar inconsistencias en los datos.

## Objetivo del proyecto

Simular el comportamiento de transacciones en una base de datos, aplicando un caso práctico de compra de boletos para un concierto de BTS.

El sistema debe manejar correctamente situaciones como falta de disponibilidad, cancelación de una compra, bloqueos entre transacciones y operaciones que tardan demasiado tiempo.

## Conceptos principales

## Transacciones

Una transacción es un conjunto de operaciones que se ejecutan como una sola unidad. Si todo se realiza correctamente, se confirma con `COMMIT`. Si ocurre un error, se revierte con `ROLLBACK`.

En este proyecto, la compra de boletos se maneja como una transacción porque se debe verificar la disponibilidad, descontar el boleto y registrar la compra de forma correcta.

## Savepoints

Un savepoint es un punto de control dentro de una transacción. Permite volver a una parte específica sin cancelar todo el proceso.

En la simulación, se puede crear un savepoint después de seleccionar o reservar un boleto. Si luego ocurre un problema, como falta de disponibilidad o error en el proceso, el sistema puede regresar a ese punto y cancelar la operación sin afectar toda la base de datos.

## Deadlock

Un deadlock ocurre cuando dos transacciones se bloquean entre sí. Por ejemplo, una transacción puede estar actualizando la disponibilidad de boletos mientras otra intenta modificar la misma información al mismo tiempo.

Cuando esto sucede, la base de datos detecta el conflicto y cancela una de las transacciones para que la otra pueda continuar.

## Timeout

Un timeout ocurre cuando una transacción tarda demasiado tiempo en completarse. La base de datos cancela la operación para evitar que el sistema quede esperando indefinidamente.

Esto es útil en sistemas de venta de boletos, donde muchos usuarios pueden intentar comprar al mismo tiempo.

## Estructura del proyecto

El repositorio contiene los siguientes archivos:

```text
simulacion_transacciones.py
README.md
requirements.txt
.gitignore
```

## Requisitos

Para ejecutar el proyecto se necesita:

Python 3.x instalado.

PostgreSQL activo.

Librería `psycopg2-binary`.

Comando para instalar la librería:

```bash
pip install psycopg2-binary
```

También se puede usar:

```bash
pip install -r requirements.txt
```

## Funcionamiento del sistema

El sistema trabaja con tablas relacionadas con la venta de boletos para el concierto de BTS.

Por ejemplo:

`boletos`: almacena la información de los boletos disponibles.

`clientes`: almacena los datos de las personas que compran boletos.

`compras`: registra las compras realizadas.

El sistema verifica si existen boletos disponibles antes de confirmar una compra. Si hay disponibilidad, se descuenta el boleto y se registra la compra. Si ocurre un error, la transacción se revierte para mantener la consistencia de los datos.

## Simulación de compra de boleto

El proceso funciona de la siguiente manera:

1. Se verifica si hay boletos disponibles.
2. Se reserva o descuenta un boleto.
3. Se crea un savepoint dentro de la transacción.
4. Se intenta registrar la compra.
5. Si todo sale bien, se confirma la transacción.
6. Si ocurre un error, se vuelve al savepoint o se realiza un rollback.

De esta manera, el sistema evita vender boletos que ya no están disponibles.

## Simulación de deadlock

Para simular un deadlock se ejecutan dos transacciones al mismo tiempo.

Una transacción intenta actualizar primero la disponibilidad de boletos y luego la compra.

Otra transacción intenta actualizar primero la compra y luego la disponibilidad de boletos.

Como ambas transacciones esperan recursos bloqueados por la otra, se produce un deadlock. La base de datos detecta el problema y cancela una de ellas.

## Simulación de timeout

La simulación de timeout consiste en configurar un tiempo máximo de espera para una operación. Si una transacción tarda demasiado, la base de datos la cancela.

Esto representa una situación real en la venta de boletos, cuando muchas personas intentan comprar entradas al mismo tiempo y el sistema puede tardar en responder.

## Resultados esperados

Compra exitosa:

```text
Boleto disponible.
Compra registrada correctamente.
Transacción confirmada.
```

Falta de disponibilidad:

```text
No hay boletos disponibles.
Rollback ejecutado.
Compra cancelada.
```

Deadlock:

```text
Deadlock detectado.
Una transacción fue cancelada.
La otra transacción continuó correctamente.
```

Timeout:

```text
Tiempo de espera agotado.
Operación cancelada.
Rollback ejecutado.
```

## Preguntas de reflexión

## 1. ¿Por qué es importante usar savepoints en transacciones largas? ¿Qué problema resuelven?

Los savepoints son importantes porque permiten regresar a un punto específico dentro de una transacción sin cancelar todo el proceso. Resuelven el problema de tener que repetir toda la operación cuando solo falló una parte.

## 2. En el escenario de venta de boletos, ¿qué pasaría si no usáramos savepoints?

Si no se usaran savepoints, el sistema podría descontar un boleto aunque la compra no se complete correctamente. Esto causaría inconsistencias, porque el boleto aparecería como vendido aunque el cliente no haya terminado la compra.

## 3. ¿Cómo se produce un deadlock en una base de datos?

Un deadlock se produce cuando dos transacciones se bloquean entre sí. En este proyecto puede ocurrir cuando dos compras intentan actualizar la disponibilidad de boletos y los registros de compra al mismo tiempo, pero en diferente orden.

La base de datos resuelve el problema cancelando una de las transacciones.

## 4. ¿Qué estrategias existen para evitar deadlocks?

Para evitar deadlocks se pueden aplicar estrategias como actualizar las tablas siempre en el mismo orden, mantener las transacciones cortas, liberar recursos rápidamente y controlar errores con rollback.

También se pueden implementar reintentos automáticos cuando una transacción falla.

## 5. ¿Qué sucede cuando una transacción alcanza el timeout?

Cuando una transacción alcanza el timeout, la base de datos cancela la operación. Esto evita que el sistema quede bloqueado por demasiado tiempo.

Para el usuario final, puede mostrarse un mensaje indicando que la compra no pudo completarse. Para manejarlo mejor, se pueden usar mensajes claros, rollback automático y reintentos controlados.

## Conclusión

Con este proyecto se comprendió cómo las transacciones ayudan a mantener la consistencia de los datos en un sistema de venta de boletos. Los savepoints permiten controlar errores parciales, los deadlocks muestran los problemas que pueden ocurrir cuando varios usuarios compran al mismo tiempo y los timeouts ayudan a evitar esperas demasiado largas.

Este tipo de control es importante en sistemas reales de venta de entradas, especialmente en conciertos con alta demanda como BTS.
