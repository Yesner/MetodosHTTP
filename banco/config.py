"""Configuración del proyecto (clave y ruta de la base SQLite)."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def obtener_configuracion():
    clave = os.getenv("BANCO_API_KEY", "")
    if not clave:
        raise RuntimeError("Falta BANCO_API_KEY. Ejecuta: python configurar.py")

    archivo_db = Path(os.getenv("BANCO_DB_PATH", str(BASE_DIR / "datos" / "banco.sqlite3")))
    archivo_db.parent.mkdir(parents=True, exist_ok=True)

    return {"BANCO_API_KEY": clave, "BANCO_DB_PATH": str(archivo_db)}
