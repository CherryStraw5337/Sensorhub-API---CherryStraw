def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convierte una temperatura de grados Celsius a grados Fahrenheit.
    
    Args:
        celsius (float): Temperatura en grados Celsius.
        
    Returns:
        float: Temperatura convertida a grados Fahrenheit.
        
    Raises:
        ValueError: Si la temperatura es menor al cero absoluto (-273.15 °C).
    """
    if celsius < -273.15:
        raise ValueError("La temperatura no puede ser inferior al cero absoluto (-273.15 °C).")
    return round((celsius * 9 / 5) + 32, 2)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convierte una temperatura de grados Fahrenheit a grados Celsius.
    
    Args:
        fahrenheit (float): Temperatura en grados Fahrenheit.
        
    Returns:
        float: Temperatura convertida a grados Celsius.
        
    Raises:
        ValueError: Si la temperatura resultante es menor al cero absoluto (-273.15 °C).
    """
    celsius = (fahrenheit - 32) * 5/9
    if celsius < -273.15:
        raise ValueError("La temperatura no puede ser inferior al cero absoluto (-273.15 °C).")
    return celsius