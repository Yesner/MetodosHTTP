"""Rutas POST para ingresar, retirar y transferir dinero simulado."""

from flask import Blueprint, jsonify

from ..servicios import operaciones as servicio
from ..validaciones import centavos_positivos, datos_json, entero_positivo

operaciones_bp = Blueprint("operaciones", __name__)


@operaciones_bp.post("/depositar")
def depositar():
    datos = datos_json()
    cuenta_id = entero_positivo(datos, "cuenta_id")
    importe = centavos_positivos(datos)
    saldo = servicio.depositar(cuenta_id, importe)
    return jsonify({"mensaje": "Depósito realizado", "saldo": saldo})


@operaciones_bp.post("/retirar")
def retirar():
    datos = datos_json()
    cuenta_id = entero_positivo(datos, "cuenta_id")
    importe = centavos_positivos(datos)
    saldo = servicio.retirar(cuenta_id, importe)
    return jsonify({"mensaje": "Retiro realizado", "saldo": saldo})


@operaciones_bp.post("/transferir")
def transferir():
    datos = datos_json()
    origen_id = entero_positivo(datos, "origen_id")
    destino_id = entero_positivo(datos, "destino_id")
    importe = centavos_positivos(datos)
    return jsonify(servicio.transferir(origen_id, destino_id, importe))
