"""Rutas para crear, consultar y listar cuentas y movimientos."""

from flask import Blueprint, jsonify

from ..servicios import cuentas as servicio
from ..validaciones import datos_json

cuentas_bp = Blueprint("cuentas", __name__)


@cuentas_bp.post("/cuentas")
def crear_cuenta():
    datos = datos_json()
    cuenta = servicio.crear_cuenta(datos.get("titular"))
    return jsonify({"mensaje": "Cuenta creada", "cuenta": cuenta}), 201


@cuentas_bp.get("/cuentas")
def listar_cuentas():
    return jsonify({"cuentas": servicio.listar_cuentas()})


@cuentas_bp.get("/cuentas/<int:cuenta_id>")
def consultar_cuenta(cuenta_id):
    return jsonify({"cuenta": servicio.consultar_cuenta(cuenta_id)})


@cuentas_bp.get("/cuentas/<int:cuenta_id>/movimientos")
def listar_movimientos(cuenta_id):
    return jsonify({"cuenta_id": cuenta_id, "movimientos": servicio.listar_movimientos(cuenta_id)})
