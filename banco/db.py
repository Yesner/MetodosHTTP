"""Conexión, transacciones y creación de tablas SQLite."""

import sqlite3
from contextlib import contextmanager

from flask import current_app


@contextmanager
def conexion():
    db = sqlite3.connect(current_app.config["BANCO_DB_PATH"], timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA busy_timeout = 10000")
    try:
        yield db
    finally:
        db.close()


@contextmanager
def transaccion():
    """Todo se confirma o se revierte; útil para transferencias."""
    with conexion() as db:
        db.execute("BEGIN IMMEDIATE")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise


def inicializar_db():
    with conexion() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titular TEXT NOT NULL,
                saldo_centavos INTEGER NOT NULL DEFAULT 0
                    CHECK (saldo_centavos >= 0),
                creada_en TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            );

            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta_id INTEGER NOT NULL REFERENCES cuentas(id),
                tipo TEXT NOT NULL CHECK (tipo IN (
                    'DEPOSITO', 'RETIRO',
                    'TRANSFERENCIA_ENVIADA', 'TRANSFERENCIA_RECIBIDA'
                )),
                monto_centavos INTEGER NOT NULL CHECK (monto_centavos > 0),
                cuenta_relacionada_id INTEGER REFERENCES cuentas(id),
                fecha TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_movimientos_cuenta
                ON movimientos(cuenta_id, id DESC);
        """)
        db.commit()
