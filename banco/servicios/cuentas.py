"""Acceso a cuentas y listado de movimientos."""

from ..db import conexion, transaccion
from ..errores import ApiError
from ..validaciones import dinero


def buscar_cuenta(db, cuenta_id):
    cuenta = db.execute(
        "SELECT id, titular, saldo_centavos, creada_en FROM cuentas WHERE id = ?",
        (cuenta_id,),
    ).fetchone()
    if cuenta is None:
        raise ApiError(f"La cuenta {cuenta_id} no existe", 404)
    return cuenta


def presentar_cuenta(cuenta):
    return {
        "id": cuenta["id"],
        "titular": cuenta["titular"],
        "saldo": dinero(cuenta["saldo_centavos"]),
        "moneda": "NIO (simulada)",
        "creada_en": cuenta["creada_en"],
    }


def crear_cuenta(titular):
    if not isinstance(titular, str) or not 2 <= len(titular.strip()) <= 80:
        raise ApiError("'titular' debe tener entre 2 y 80 caracteres")
    with transaccion() as db:
        cursor = db.execute(
            "INSERT INTO cuentas (titular) VALUES (?)", (titular.strip(),)
        )
        cuenta = buscar_cuenta(db, cursor.lastrowid)
        return presentar_cuenta(cuenta)


def listar_cuentas():
    with conexion() as db:
        filas = db.execute(
            "SELECT id, titular, saldo_centavos, creada_en FROM cuentas ORDER BY id"
        ).fetchall()
        return [presentar_cuenta(fila) for fila in filas]


def consultar_cuenta(cuenta_id):
    with conexion() as db:
        return presentar_cuenta(buscar_cuenta(db, cuenta_id))


def listar_movimientos(cuenta_id):
    with conexion() as db:
        buscar_cuenta(db, cuenta_id)
        filas = db.execute(
            """SELECT id, tipo, monto_centavos, cuenta_relacionada_id, fecha
               FROM movimientos WHERE cuenta_id = ?
               ORDER BY id DESC LIMIT 50""",
            (cuenta_id,),
        ).fetchall()
        return [
            {
                "id": fila["id"],
                "tipo": fila["tipo"],
                "monto": dinero(fila["monto_centavos"]),
                "cuenta_relacionada_id": fila["cuenta_relacionada_id"],
                "fecha": fila["fecha"],
            }
            for fila in filas
        ]
