"""Pruebas unitarias para las funciones de conversión de sensores."""

import pytest

from semana5.conversions import celsius_to_fahrenheit


def test_celsius_to_fahrenheit_freezing_point() -> None:
    """Verifica la conversión en el punto de congelación del agua (0 C -> 32 F)."""
    assert celsius_to_fahrenheit(0.0) == 32.0


def test_celsius_to_fahrenheit_boiling_point() -> None:
    """Verifica la conversión en el punto de ebullición del agua (100 C -> 212 F)."""
    assert celsius_to_fahrenheit(100.0) == 212.0


def test_celsius_to_fahrenheit_negative_temperature() -> None:
    """Verifica la conversión con valores negativos donde ambas escalas se cruzan."""
    assert celsius_to_fahrenheit(-40.0) == -40.0


def test_celsius_to_fahrenheit_precision_rounding() -> None:
    """Verifica que el resultado esté redondeado estrictamente a 2 decimales."""
    assert celsius_to_fahrenheit(36.6) == 97.88


def test_celsius_to_fahrenheit_absolute_zero() -> None:
    """Verifica la conversión en el límite exacto del cero absoluto."""
    assert celsius_to_fahrenheit(-273.15) == -459.67


def test_celsius_to_fahrenheit_impossible_temperature() -> None:
    """Verifica el manejo de errores ante temperaturas físicas imposibles."""
    with pytest.raises(ValueError, match="inferior al cero absoluto"):
        celsius_to_fahrenheit(-274.0)