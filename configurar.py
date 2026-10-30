"""Crea una clave aleatoria para probar la API sin subirla a GitHub."""
from pathlib import Path
from secrets import token_urlsafe

archivo = Path(__file__).resolve().parent / ".env"
if archivo.exists():
    print("El archivo .env ya existe. No lo voy a sobrescribir.")
else:
    clave = token_urlsafe(32)
    archivo.write_text(f"BANCO_API_KEY={clave}\n", encoding="utf-8")
    archivo.chmod(0o600)
    print("Creado .env con una clave aleatoria de prueba.")
    print(f"X-API-Key: {clave}")
    print("Guarda esta clave. Compártela solo con las personas autorizadas a probar la API.")
