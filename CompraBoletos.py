import psycopg2
import threading
import time


# Conexion Base
def nueva_conexion():
    return psycopg2.connect(
        database="boletos_bts",
        user="emilia",
        password="root",
        host="localhost",
        port="5432"
    )


# Compra de boleto con SAVEPOINT
def comprar_boleto(id_concierto, id_asiento, id_pago):
    conn = nueva_conexion()
    cur = conn.cursor()

    try:
        print("\nINICIANDO COMPRA DE BOLETO BTS")

        cur.execute("BEGIN;")
        cur.execute("SET statement_timeout = '5000';")

        # Concierto
        print("Verificando boletos disponibles...")

        cur.execute("""
            SELECT boletos_disponibles
            FROM conciertos
            WHERE id_concierto = %s
            FOR UPDATE;
        """, (id_concierto,))

        concierto = cur.fetchone()

        if not concierto or concierto[0] <= 0:
            raise Exception("No hay boletos disponibles")

        cur.execute("""
            UPDATE conciertos
            SET boletos_disponibles = boletos_disponibles - 1
            WHERE id_concierto = %s;
        """, (id_concierto,))

        cur.execute("SAVEPOINT sp_boleto;")
        print("SAVEPOINT sp_boleto creado")

        # Asiento
        print("Reservando asiento...")

        cur.execute("""
            SELECT disponible
            FROM asientos
            WHERE id_asiento = %s
            FOR UPDATE;
        """, (id_asiento,))

        asiento = cur.fetchone()

        if not asiento or asiento[0] is False:
            print("Asiento no disponible. Rollback al boleto")

            cur.execute("ROLLBACK TO SAVEPOINT sp_boleto;")

            cur.execute("""
                UPDATE conciertos
                SET boletos_disponibles = boletos_disponibles + 1
                WHERE id_concierto = %s;
            """, (id_concierto,))

            raise Exception("Compra cancelada por asiento no disponible")

        cur.execute("""
            UPDATE asientos
            SET disponible = FALSE
            WHERE id_asiento = %s;
        """, (id_asiento,))

        cur.execute("SAVEPOINT sp_asiento;")
        print("SAVEPOINT sp_asiento creado")

        # Pago
        print("Procesando pago...")

        cur.execute("""
            SELECT disponible
            FROM pagos
            WHERE id_pago = %s
            FOR UPDATE;
        """, (id_pago,))

        pago = cur.fetchone()

        if not pago or pago[0] is False:
            print("Pago rechazado. Rollback al asiento")

            cur.execute("ROLLBACK TO SAVEPOINT sp_asiento;")

            raise Exception("Compra cancelada por error en el pago")

        cur.execute("""
            UPDATE pagos
            SET disponible = FALSE
            WHERE id_pago = %s;
        """, (id_pago,))

        conn.commit()

        print("COMPRA DE BOLETO BTS COMPLETADA CON EXITO")

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)

    finally:
        cur.close()
        conn.close()


# Ejemplo con DEADLOCK
def deadlock_1():
    conn = nueva_conexion()
    cur = conn.cursor()
    conn.autocommit = False

    try:
        print("\nT1 bloquea conciertos")

        cur.execute("""
            SELECT *
            FROM conciertos
            WHERE id_concierto = 1
            FOR UPDATE;
        """)

        time.sleep(5)

        print("T1 intenta bloquear asientos")

        cur.execute("""
            SELECT *
            FROM asientos
            WHERE id_asiento = 1
            FOR UPDATE;
        """)

        conn.commit()

    except Exception as e:
        print("DEADLOCK T1:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def deadlock_2():
    conn = nueva_conexion()
    cur = conn.cursor()
    conn.autocommit = False

    try:
        print("\nT2 bloquea asientos")

        cur.execute("""
            SELECT *
            FROM asientos
            WHERE id_asiento = 1
            FOR UPDATE;
        """)

        time.sleep(5)

        print("T2 intenta bloquear conciertos")

        cur.execute("""
            SELECT *
            FROM conciertos
            WHERE id_concierto = 1
            FOR UPDATE;
        """)

        conn.commit()

    except Exception as e:
        print("DEADLOCK T2:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def simular_deadlock():
    t1 = threading.Thread(target=deadlock_1)
    t2 = threading.Thread(target=deadlock_2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


# TIMEOUT
def compra_lenta():
    conn = nueva_conexion()
    cur = conn.cursor()
    conn.autocommit = False

    try:
        print("\nT1 procesando compra lenta")

        cur.execute("SELECT pg_sleep(8);")

        conn.commit()

    except Exception as e:
        print("ERROR T1:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def compra_intenta():
    time.sleep(2)

    conn = nueva_conexion()
    cur = conn.cursor()
    conn.autocommit = False

    try:
        print("T2 intenta comprar boleto")

        cur.execute("SET statement_timeout = '3000';")

        cur.execute("SELECT pg_sleep(6);")

        conn.commit()

    except Exception as e:
        print("TIMEOUT:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def simular_timeout():
    t1 = threading.Thread(target=compra_lenta)
    t2 = threading.Thread(target=compra_intenta)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    print("\n==============================")
    print(" SISTEMA DE BOLETOS BTS")
    print("==============================")

    comprar_boleto(1, 1, 1)

    simular_deadlock()

    simular_timeout()
