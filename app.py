"""Archivo de entrada: inicia la aplicación Flask."""

from banco import crear_app

app = crear_app()

if __name__ == "__main__":
    # Codespaces expone el puerto 5000 mediante su URL HTTPS.
    app.run(host="0.0.0.0", port=5000, debug=False)
