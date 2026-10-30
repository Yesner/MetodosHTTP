"""Crea Flask, configura la base de datos y registra las rutas."""

import secrets

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from .config import obtener_configuracion
from .db import inicializar_db
from .errores import ApiError
from .rutas.cuentas import cuentas_bp
from .rutas.documentacion import documentacion_bp
from .rutas.operaciones import operaciones_bp
from .rutas.salud import salud_bp


def crear_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.update(obtener_configuracion())

    @app.before_request
    def exigir_clave():
        if request.path in {"/salud", "/docs", "/docs/", "/openapi.json"}:
            return None
        clave_recibida = request.headers.get("X-API-Key", "")
        if not secrets.compare_digest(clave_recibida, app.config["BANCO_API_KEY"]):
            raise ApiError("Clave de API ausente o incorrecta", 401)
        return None

    @app.errorhandler(ApiError)
    def error_de_api(error):
        return jsonify({"error": error.mensaje}), error.status

    @app.errorhandler(HTTPException)
    def error_http(error):
        return jsonify({"error": error.description}), error.code

    app.register_blueprint(salud_bp)
    app.register_blueprint(documentacion_bp)
    app.register_blueprint(cuentas_bp)
    app.register_blueprint(operaciones_bp)

    with app.app_context():
        inicializar_db()

    return app
