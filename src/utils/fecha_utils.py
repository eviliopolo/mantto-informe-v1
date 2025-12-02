"""
Utilidades para manejo de fechas en español
"""
from datetime import datetime, date
from typing import Union, Any, List, Dict
import config
import logging
import re

logger = logging.getLogger(__name__)


def formatear_fecha_simple(fecha: Any) -> str:
    """
    Formatea una fecha al formato d/m/yyyy (ej: 6/11/2025)
    Sin ceros a la izquierda en día y mes
    
    Args:
        fecha: Puede ser datetime, string (YYYY-MM-DD, DD/MM/YYYY, etc), pandas Timestamp, o None
        
    Returns:
        Fecha formateada como "d/m/yyyy" o cadena vacía si no es válida
    """
    if not fecha or fecha == "":
        return ""
    
    try:
        # Si ya es datetime, formatearlo directamente
        if isinstance(fecha, datetime):
            # Formatear como d/m/yyyy sin ceros a la izquierda
            dia = str(fecha.day)
            mes = str(fecha.month)
            anio = str(fecha.year)
            return f"{dia}/{mes}/{anio}"
        
        # Si es string, intentar parsear diferentes formatos
        if isinstance(fecha, str):
            # Limpiar espacios
            fecha = fecha.strip()
            
            # Si ya está en formato d/m/yyyy sin ceros, retornarlo tal cual
            # Verificar patrón d/m/yyyy (ej: 6/11/2025)
            if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', fecha):
                return fecha
            
            # Intentar parsear diferentes formatos (incluyendo datetime con hora)
            # IMPORTANTE: Ordenar de más específico a menos específico
            formatos_posibles = [
                "%Y-%m-%dT%H:%M:%S.%f",  # 2025-11-01T00:00:00.000000 (formato ISO con microsegundos)
                "%Y-%m-%dT%H:%M:%S",      # 2025-11-01T00:00:00 (formato ISO datetime)
                "%Y-%m-%d %H:%M:%S.%f",  # 2025-11-06 00:00:00.000000
                "%Y-%m-%d %H:%M:%S",      # 2025-11-06 00:00:00
                "%Y-%m-%d",              # 2025-11-06
                "%d/%m/%Y",              # 06/11/2025
                "%d-%m-%Y",              # 06-11-2025
                "%Y/%m/%d",              # 2025/11/06
                "%d/%m/%y",              # 06/11/25
                "%m/%d/%Y",              # 11/06/2025 (formato US)
            ]
            
            # Intentar parsear con los formatos posibles
            fecha_obj = None
            for formato in formatos_posibles:
                try:
                    fecha_obj = datetime.strptime(fecha, formato)
                    break
                except ValueError:
                    continue
            
            if fecha_obj:
                # Formatear como d/m/yyyy (sin ceros a la izquierda)
                return f"{fecha_obj.day}/{fecha_obj.month}/{fecha_obj.year}"
            else:
                # Si no se puede parsear, retornar tal cual
                return str(fecha)
        
        # Si es otro tipo (pandas Timestamp, etc), intentar convertirlo
        else:
            # Intentar manejar pandas Timestamp
            try:
                import pandas as pd
                if isinstance(fecha, pd.Timestamp):
                    return f"{fecha.day}/{fecha.month}/{fecha.year}"
            except (ImportError, AttributeError):
                pass
            
            # Intentar convertir a string y parsear
            fecha_str = str(fecha)
            # Intentar parsear diferentes formatos (incluyendo ISO datetime)
            formatos_intento = [
                "%Y-%m-%dT%H:%M:%S",      # 2025-11-01T00:00:00 (formato ISO)
                "%Y-%m-%dT%H:%M:%S.%f",  # 2025-11-01T00:00:00.000000
                "%Y-%m-%d %H:%M:%S",      # 2025-11-06 00:00:00
                "%Y-%m-%d",              # 2025-11-06
            ]
            for formato in formatos_intento:
                try:
                    fecha_obj = datetime.strptime(fecha_str, formato)
                    return f"{fecha_obj.day}/{fecha_obj.month}/{fecha_obj.year}"
                except ValueError:
                    continue
            return fecha_str
            
    except Exception as e:
        logger.warning(f"Error al formatear fecha '{fecha}': {e}")
        return str(fecha) if fecha else ""


def formatear_fechas_en_tabla(tabla: List[Dict[str, Any]], campos_fecha: List[str]) -> List[Dict[str, Any]]:
    """
    Formatea los campos de fecha en una tabla al formato d/m/yyyy
    
    Args:
        tabla: Lista de diccionarios con los datos de la tabla
        campos_fecha: Lista de nombres de campos que contienen fechas (pueden tener variaciones)
        
    Returns:
        Tabla con las fechas formateadas
    """
    if not tabla:
        return tabla
    
    tabla_formateada = []
    for registro in tabla:
        registro_formateado = registro.copy()
        
        # Buscar campos de fecha con diferentes variaciones (case-insensitive, con/sin espacios)
        campos_encontrados = set()
        for campo_fecha_buscado in campos_fecha:
            # Buscar el campo exacto
            if campo_fecha_buscado in registro_formateado:
                campos_encontrados.add(campo_fecha_buscado)
            else:
                # Buscar variaciones del nombre del campo (case-insensitive, con/sin espacios)
                campo_lower = campo_fecha_buscado.lower().replace("_", " ").replace("-", " ")
                for key in registro_formateado.keys():
                    key_normalized = key.lower().replace("_", " ").replace("-", " ")
                    if campo_lower == key_normalized or campo_lower in key_normalized or key_normalized in campo_lower:
                        campos_encontrados.add(key)
                        break
                # También buscar campos que contengan "fecha" si el campo buscado contiene "fecha"
                if "fecha" in campo_lower:
                    for key in registro_formateado.keys():
                        if "fecha" in key.lower():
                            campos_encontrados.add(key)
        
        # Formatear todos los campos de fecha encontrados
        for campo_fecha in campos_encontrados:
            if campo_fecha in registro_formateado:
                valor_original = registro_formateado[campo_fecha]
                valor_formateado = formatear_fecha_simple(valor_original)
                registro_formateado[campo_fecha] = valor_formateado
                # Log para debugging si la fecha no se formateó correctamente
                if valor_original and valor_formateado == str(valor_original) and ("00:00:00" in str(valor_original) or "T" in str(valor_original)):
                    logger.warning(f"Fecha no formateada correctamente en campo '{campo_fecha}': {valor_original} -> {valor_formateado}")
        
        tabla_formateada.append(registro_formateado)
    
    return tabla_formateada


def fecha_texto_largo(fecha: Union[datetime, date, str]) -> str:
    """
    Convierte fecha a texto largo en español
    Ejemplo: "23 de septiembre de 2025"
    """
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    dia = fecha.day
    mes = config.MESES[fecha.month].lower()
    anio = fecha.year
    
    return f"{dia} de {mes} de {anio}"

def fecha_texto_corto(fecha: Union[datetime, date, str]) -> str:
    """
    Convierte fecha a texto corto
    Ejemplo: "23/09/2025"
    """
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    return fecha.strftime("%d/%m/%Y")

def periodo_texto(anio: int, mes: int) -> str:
    """
    Retorna el periodo en formato texto
    Ejemplo: "Septiembre de 2025"
    """
    return f"{config.MESES[mes]} de {anio}"

def rango_mes(anio: int, mes: int) -> tuple:
    """
    Retorna el primer y último día del mes
    """
    from calendar import monthrange
    
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, monthrange(anio, mes)[1])
    
    return primer_dia, ultimo_dia


