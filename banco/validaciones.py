"""Comprueba JSON, identificadores y cantidades de dinero."""

from decimal import Decimal, InvalidOperation

from flask import request

from .errores import ApiError


def datos_json():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise ApiError("Envía un objeto JSON válido con Content-Type: application/json")
    return datos


def entero_positivo(datos, campo):
    valor = datos.get(campo)
    if type(valor) is not int or valor <= 0:
        raise ApiError(f"'{campo}' debe ser un número entero positivo")
    return valor


def centavos_positivos(datos):
    valor = datos.get("monto")
    if not isinstance(valor, str) or not valor.strip():
        raise ApiError("'monto' debe ser texto decimal, ejemplo: '150.50'")
    try:
        importe = Decimal(valor)
    except InvalidOperation:
        raise ApiError("'monto' no es un número decimal válido") from None
    if not importe.is_finite() or importe <= 0 or importe > Decimal("1000000000"):
        raise ApiError("'monto' debe ser mayor que cero y como máximo 1000000000")
    total_centavos = importe * 100
    if total_centavos != total_centavos.to_integral_value():
        raise ApiError("'monto' admite como máximo 2 decimales")
    return int(total_centavos)


def dinero(centavos):
    """Presenta cantidades sin usar valores flotantes."""
    return f"{centavos // 100}.{centavos % 100:02d}"
