"""Rutas de la documentación interactiva; no alteran las operaciones bancarias."""

import json
from pathlib import Path

from flask import Blueprint, jsonify, render_template

documentacion_bp = Blueprint("documentacion", __name__)
ARCHIVO_ESPECIFICACION = Path(__file__).resolve().parent.parent / "docs" / "openapi.json"


@documentacion_bp.get("/docs")
@documentacion_bp.get("/docs/")
def swagger_ui():
    """Interfaz Swagger UI sin clave; el servidor exige clave para hacer operaciones."""
    return render_template("swagger.html")


@documentacion_bp.get("/openapi.json")
def openapi():
    """Documento OpenAPI 3 que Swagger UI consume para mostrar rutas y ejemplos."""
    with ARCHIVO_ESPECIFICACION.open(encoding="utf-8") as archivo:
        especificacion = json.load(archivo)
    respuesta = jsonify(especificacion)
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta
