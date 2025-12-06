"""
Utilidades para formateo de valores monetarios
"""
from num2words import num2words
from typing import Union


def numero_a_letras(numero: Union[int, float], incluir_moneda: bool = True) -> str:
    """
    Convierte un número a su representación en letras en español
    
    Args:
        numero: Valor numérico
        incluir_moneda: Si True, agrega "PESOS M/CTE"
    
    Returns:
        Texto en mayúsculas
        Ejemplo: "CINCUENTA Y SEIS MILLONES NOVECIENTOS NUEVE MIL PESOS M/CTE"
    """
    try:
        # Validar que el número sea válido
        if numero is None:
            return "CERO PESOS M/CTE" if incluir_moneda else "CERO"
        
        parte_entera = int(abs(numero))  # Usar valor absoluto para evitar problemas
        
        # Si es cero, retornar directamente
        if parte_entera == 0:
            return "CERO PESOS M/CTE" if incluir_moneda else "CERO"
        
        texto = num2words(parte_entera, lang='es')
        texto = texto.upper()
        
        # Limpiar texto
        texto = texto.replace(" Y ", " Y ")
        
        if incluir_moneda:
            texto += " PESOS M/CTE"
        
        return texto
    except Exception as e:
        # Si hay error, retornar formato numérico como fallback
        try:
            return f"{numero:,.0f}".replace(",", ".")
        except:
            return "CERO PESOS M/CTE" if incluir_moneda else "CERO"


def formato_moneda_cop(numero: Union[int, float]) -> str:
    """
    Formatea número como moneda colombiana
    
    Args:
        numero: Valor numérico
    
    Returns:
        String formateado: "$56.909.324"
    """
    try:
        # Validar que el número sea válido
        if numero is None:
            return "$0"
        
        # Asegurar que sea un número
        num_valor = float(numero)
        
        # Formatear con separadores de miles
        # Python usa coma como separador, Colombia usa punto
        texto = f"{num_valor:,.0f}"
        # Reemplazar: coma -> temporal, punto -> coma, temporal -> punto
        texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"${texto}"
    except (ValueError, TypeError):
        return "$0"


def formato_cantidad(numero: Union[int, float], decimales: int = 0) -> str:
    """
    Formatea cantidad con separadores de miles
    
    Args:
        numero: Valor numérico
        decimales: Cantidad de decimales
    
    Returns:
        String formateado: "1.234" o "1.234,56"
    """
    if decimales > 0:
        formato = f"{{:,.{decimales}f}}"
        texto = formato.format(numero)
    else:
        texto = f"{numero:,.0f}"
    
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")

