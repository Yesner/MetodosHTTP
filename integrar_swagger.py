"""Integra Swagger en un proyecto Banco Demo modular sin reemplazar app.py ni la base de datos.

Ejecuta `python integrar_swagger.py` desde la raíz del proyecto.
"""
from pathlib import Path
import sys

archivo = Path(__file__).resolve().parent / "banco" / "__init__.py"
if not archivo.is_file():
    sys.exit("No se encontró banco/__init__.py. Ejecuta el script desde el proyecto modular.")
contenido = archivo.read_text(encoding="utf-8")
original = contenido

if "from .rutas.documentacion import documentacion_bp" not in contenido:
    referencia = "from .rutas.cuentas import cuentas_bp\n"
    if referencia not in contenido:
        sys.exit("No encuentro dónde importar el Blueprint. No se modificó el archivo.")
    contenido = contenido.replace(referencia, referencia + "from .rutas.documentacion import documentacion_bp\n", 1)

if 'if request.path in {"/salud", "/docs", "/docs/", "/openapi.json"}:' not in contenido:
    referencia = 'if request.path == "/salud":'
    if referencia not in contenido:
        sys.exit("No encuentro la excepción de autenticación. No se modificó el archivo.")
    contenido = contenido.replace(referencia, 'if request.path in {"/salud", "/docs", "/docs/", "/openapi.json"}:', 1)

if "app.register_blueprint(documentacion_bp)" not in contenido:
    referencia = "    app.register_blueprint(salud_bp)\n"
    if referencia not in contenido:
        sys.exit("No encuentro dónde registrar el Blueprint. No se modificó el archivo.")
    contenido = contenido.replace(referencia, referencia + "    app.register_blueprint(documentacion_bp)\n", 1)

if contenido == original:
    print("Swagger ya estaba integrado. No se hicieron cambios.")
else:
    respaldo = archivo.with_suffix(".py.respaldo_antes_swagger")
    if not respaldo.exists():
        respaldo.write_text(original, encoding="utf-8")
    archivo.write_text(contenido, encoding="utf-8")
    print("Swagger integrado sin borrar tu base de datos ni .env.")
    print("Se guardó una copia de seguridad de banco/__init__.py.")
print("Reinicia Flask y visita /docs en el puerto 5000.")
