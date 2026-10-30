"""Endpoint público para comprobar si la API está activa."""

from flask import Blueprint, jsonify

salud_bp = Blueprint("salud", __name__)


@salud_bp.get("/salud")
def salud():
    return jsonify({"estado": "ok", "servicio": "Banco Demo SQLite"})
