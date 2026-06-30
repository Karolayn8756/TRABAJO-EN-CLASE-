## Preguntas de reflexión

### 1. ¿Por qué es importante usar savepoints en transacciones largas? ¿Qué problema resuelven?

Los savepoints son importantes porque permiten regresar a un punto específico dentro de una transacción sin deshacer todo el proceso. Sirven para controlar errores parciales y evitar que la base de datos quede en un estado incorrecto.

### 2. En el escenario de reserva, ¿qué pasaría si no usáramos savepoints y el hotel no tuviera cupo?

Si no se usaran savepoints, el sistema podría descontar el asiento del vuelo aunque la reserva del hotel falle. Esto generaría una reserva incompleta y afectaría la consistencia de los datos, porque habría menos disponibilidad de vuelos sin que el paquete turístico se haya completado.

### 3. ¿Cómo se produce un deadlock en una base de datos? Explica el ejemplo implementado y cómo se resolvió.

Un deadlock ocurre cuando dos transacciones se bloquean entre sí porque cada una espera que la otra libere un recurso. En el ejemplo, una transacción bloquea primero vuelos y luego hoteles, mientras otra bloquea primero hoteles y luego vuelos. PostgreSQL detecta el deadlock y cancela una de las transacciones para que la otra pueda continuar.

### 4. ¿Qué estrategias existen para evitar deadlocks en sistemas concurrentes?

Algunas estrategias son: acceder siempre a las tablas en el mismo orden, mantener las transacciones lo más cortas posible, usar bloqueos solo cuando sea necesario, aplicar timeouts y manejar errores con rollback o reintentos controlados.

### 5. ¿Qué sucede cuando una transacción alcanza el timeout?

Cuando una transacción alcanza el timeout, la base de datos cancela la operación porque esperó demasiado tiempo. Esto evita bloqueos prolongados, pero puede afectar al usuario si no recibe una respuesta clara. Para manejarlo, se pueden mostrar mensajes de error, hacer rollback, registrar el fallo y permitir reintentar la operación.
