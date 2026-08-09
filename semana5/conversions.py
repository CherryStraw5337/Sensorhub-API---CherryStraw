"""Módulo de funciones puras para la conversión de mediciones de sensores."""


def celsius_to_fahrenheit(c: float) -> float:
    """Convierte una temperatura de grados Celsius a Fahrenheit.

    Args:
        c (float): Temperatura en grados Celsius.

    Returns:
        float: Temperatura en grados Fahrenheit, redondeada a 2 decimales.

    Raises:
        ValueError: Si la temperatura es inferior al cero absoluto (-273.15 C).
    """
    if c < -273.15:
        raise ValueError("Temperatura inferior al cero absoluto no es físicamente posible.")

    fahrenheit: float = (c * 9.0 / 5.0) + 32.0
    return round(fahrenheit, 2)