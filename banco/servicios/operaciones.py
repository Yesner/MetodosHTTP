"""Depósitos, retiros y transferencias con transacciones SQLite."""

from ..db import transaccion
from ..errores import ApiError
from ..validaciones import dinero
from .cuentas import buscar_cuenta


def depositar(cuenta_id, importe):
    with transaccion() as db:
        cuenta = buscar_cuenta(db, cuenta_id)
        db.execute(
            "UPDATE cuentas SET saldo_centavos = saldo_centavos + ? WHERE id = ?",
            (importe, cuenta_id),
        )
        db.execute(
            "INSERT INTO movimientos (cuenta_id, tipo, monto_centavos) VALUES (?, ?, ?)",
            (cuenta_id, "DEPOSITO", importe),
        )
        return dinero(cuenta["saldo_centavos"] + importe)


def retirar(cuenta_id, importe):
    with transaccion() as db:
        cuenta = buscar_cuenta(db, cuenta_id)
        if cuenta["saldo_centavos"] < importe:
            raise ApiError("Fondos insuficientes", 409)
        db.execute(
            "UPDATE cuentas SET saldo_centavos = saldo_centavos - ? WHERE id = ?",
            (importe, cuenta_id),
        )
        db.execute(
            "INSERT INTO movimientos (cuenta_id, tipo, monto_centavos) VALUES (?, ?, ?)",
            (cuenta_id, "RETIRO", importe),
        )
        return dinero(cuenta["saldo_centavos"] - importe)


def transferir(origen_id, destino_id, importe):
    if origen_id == destino_id:
        raise ApiError("Las cuentas de origen y destino deben ser diferentes")

    with transaccion() as db:
        origen = buscar_cuenta(db, origen_id)
        buscar_cuenta(db, destino_id)
        if origen["saldo_centavos"] < importe:
            raise ApiError("Fondos insuficientes", 409)
        db.execute(
            "UPDATE cuentas SET saldo_centavos = saldo_centavos - ? WHERE id = ?",
            (importe, origen_id),
        )
        db.execute(
            "UPDATE cuentas SET saldo_centavos = saldo_centavos + ? WHERE id = ?",
            (importe, destino_id),
        )
        db.execute(
            """INSERT INTO movimientos
               (cuenta_id, tipo, monto_centavos, cuenta_relacionada_id)
               VALUES (?, ?, ?, ?)""",
            (origen_id, "TRANSFERENCIA_ENVIADA", importe, destino_id),
        )
        db.execute(
            """INSERT INTO movimientos
               (cuenta_id, tipo, monto_centavos, cuenta_relacionada_id)
               VALUES (?, ?, ?, ?)""",
            (destino_id, "TRANSFERENCIA_RECIBIDA", importe, origen_id),
        )
        saldo_origen = origen["saldo_centavos"] - importe

    return {
        "mensaje": "Transferencia realizada",
        "monto": dinero(importe),
        "origen_id": origen_id,
        "destino_id": destino_id,
        "saldo_origen": dinero(saldo_origen),
    }
