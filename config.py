"""
Configuración global unificada del sistema
Centraliza todas las configuraciones del sistema, incluyendo variables de entorno
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================================================================
# DIRECTORIOS
# ============================================================================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "src" / "resources" / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "src" / "resources" / "templates"
FUENTES_DIR = BASE_DIR / "data" / "fuentes"
FIJOS_DIR = BASE_DIR / "src" / "resources" / "data" / "fijos"
INFORMES_APROBADOS_DIR = BASE_DIR / "docs" / "informesAprobados"


# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# ============================================================================
# CONFIGURACIÓN CORS
# ============================================================================
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:5001,http://localhost:3000,http://localhost:5173,http://localhost:8000"
).split(",")

# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS (MongoDB)
# ============================================================================
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "mantto_informe")
MONGODB_AUTH_SOURCE = os.getenv(
    "MONGODB_AUTH_SOURCE", "admin"
)  # Base de datos de autenticación


# Construir URI de MongoDB
def _build_mongodb_uri() -> str:
    """Construye la URI de MongoDB con o sin autenticación"""
    if MONGODB_USER and MONGODB_PASSWORD:
        # URI con autenticación
        return f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}?authSource={MONGODB_AUTH_SOURCE}"
    else:
        # URI sin autenticación (desarrollo local)
        return f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}"


# URI completa de MongoDB
# Si MONGODB_URI está definida en .env, se usa esa (permite URI completa personalizada)
# Si no, se construye automáticamente con las variables individuales
MONGODB_URI = os.getenv("MONGODB_URI") or _build_mongodb_uri()

# ============================================================================
# CONFIGURACIÓN JWT
# ============================================================================
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_IN_HOURS = int(os.getenv("JWT_EXPIRES_IN_HOURS", "24"))

# ============================================================================
# CONFIGURACIÓN API EXTERNA DE AUTENTICACIÓN
# ============================================================================
EXTERNAL_AUTH_API_URL = os.getenv("EXTERNAL_AUTH_API_URL", "http://localhost:4000")
EXTERNAL_AUTH_API_TIMEOUT = int(os.getenv("EXTERNAL_AUTH_API_TIMEOUT", "10"))

# ============================================================================
# CONFIGURACIÓN GLPI
# ============================================================================
GLPI_API_URL = os.getenv("GLPI_API_URL", "https://glpi.etb.com.co/apirest.php")
GLPI_API_TOKEN = os.getenv("GLPI_API_TOKEN", "TU_TOKEN_AQUI")

# ============================================================================
# INFORMACIÓN DEL CONTRATO (FIJO)
# Datos oficiales del contrato SCJ-1809-2024
# ============================================================================
CONTRATO = {
    "numero": "SCJ-1809-2024",
    "numero_proceso": "SECOP II SCJ-SIF-CD-480-2024",
    "entidad": "EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P.",
    "entidad_corto": "ETB",
    "nit_entidad": "899.999.115-8",
    "razon_social": "EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A E.S.P. - ETB S.A E.S.P.",
    "direccion": "NIZA, CALLE 126 60 32 | PISO 1",
    "ciudad": "BOGOTÁ – COLOMBIA",
    "telefono": "6012423499",
    "objeto": "PRESTACIÓN DE LOS SERVICIOS DE ADMINISTRACIÓN, SOPORTE, MANTENIMIENTO PREVENTIVO, CORRECTIVO Y/O DE ACTUALIZACIÓN AL SISTEMA DE VIDEO VIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS",
    "objeto_corto": "MANTENIMIENTO PREVENTIVO, MANTENIMIENTO CORRECTIVO Y SOPORTE AL SISTEMA DE VIDEOVIGILANCIA DE BOGOTÁ D.C., CON DISPONIBILIDAD DE BOLSA DE REPUESTOS",
    "contratista": os.getenv("CONTRATO_CONTRATISTA", "NOMBRE DEL CONTRATISTA"),
    "nit_contratista": os.getenv("CONTRATO_NIT_CONTRATISTA", "XXX.XXX.XXX-X"),
    "supervisor": os.getenv("CONTRATO_SUPERVISOR", "NOMBRE DEL SUPERVISOR"),
    "interventor": os.getenv("CONTRATO_INTERVENTOR", "NOMBRE DEL INTERVENTOR"),
    "fecha_inicio": "2024-11-19",  # 19 de noviembre de 2024 (fecha acta de inicio)
    "fecha_fin": "2025-11-18",  # 18 de noviembre de 2025
    "fecha_suscripcion": "2024-10-31",  # 31 de octubre de 2024
    "plazo_ejecucion": "DOCE (12) MESES",
    "valor_inicial": 16450000000,  # $16.450.000.000
    "adicion_1": 2000000000,  # $2.000.000.000
    "valor_total": 18450000000,  # $18.450.000.000
    "valor_contrato": 18450000000,  # Total del contrato
    "vigencia_poliza_inicial_inicio": "2024-10-31",
    "vigencia_poliza_inicial_fin": "2028-10-31",
    "vigencia_poliza_acta_inicio": "2024-11-19",
    "vigencia_poliza_acta_fin": "2028-11-19",
    "umbral_ans": 98.9,  # Porcentaje mínimo de disponibilidad
}

# ============================================================================
# DATOS ESTÁTICOS
# ============================================================================

# Meses en español
MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

# Lista de meses en español (para compatibilidad)
MESES_LISTA = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

# Subsistemas del contrato
SUBSISTEMAS = [
    "Domos Ciudadanos",
    "TransMilenio",
    "Instituciones Educativas",
    "Centro de Traslado por Protección (CTP)",
    "Centro de Atención Inmediata (CAI)",
    "Estaciones de Policía",
    "Estadio Nemesio Camacho El Campín",
    "Centros de Monitoreo",
    "Data Center",
    "C4-CAD",
]

# Localidades de Bogotá
LOCALIDADES = [
    "Usaquén",
    "Chapinero",
    "Santa Fe",
    "San Cristóbal",
    "Usme",
    "Tunjuelito",
    "Bosa",
    "Kennedy",
    "Fontibón",
    "Engativá",
    "Suba",
    "Barrios Unidos",
    "Teusaquillo",
    "Los Mártires",
    "Antonio Nariño",
    "Puente Aranda",
    "La Candelaria",
    "Rafael Uribe Uribe",
    "Ciudad Bolívar",
    "Sumapaz",
]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def get_nombre_informe(anio: int, mes: int, version: int = 1) -> str:
    """Genera el nombre del archivo de informe"""
    nombre_mes = MESES[mes].upper()
    return f"INFORME_MENSUAL_{nombre_mes}_{anio}_V{version}.docx"


def get_periodo_texto(anio: int, mes: int) -> str:
    """Retorna el periodo en formato texto: 'Septiembre de 2025'"""
    return f"{MESES[mes]} de {anio}"

# ============================================================================
# LOGGER
# ============================================================================
logger = logging.getLogger(__name__)

def _cargar_config_carpetas_sharepoint() -> Dict:
    """
    Carga la configuración de carpetas de SharePoint desde el archivo JSON
    
    Returns:
        Diccionario con la configuración de carpetas
    """
    import json
    
    config_path = DATA_DIR / "config_carpetas_sharepoint.json"
    
    if not config_path.exists():
        logger.warning(f"Archivo de configuración no encontrado: {config_path}")
        # Retornar configuración por defecto (fallback)
        return {
            "carpetas_periodo": [],
            "ruta_base": "01 OBLIGACIONES GENERALES",
            "subcarpetas": {
                "laboratorio": "OBLIGACIÓN 2,5,6,9,13/ANEXO LABORATORIO",
                "comunicados_emitidos": "OBLIGACIÓN 7 y 10 / COMUNICADOS EMITIDOS",
                "comunicados_recibidos": "OBLIGACIÓN 7 y 10 / COMUNICADOS RECIBIDOS"
            }
        }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error al cargar configuración de carpetas SharePoint: {e}")
        # Retornar configuración por defecto
        return {
            "carpetas_periodo": [],
            "ruta_base": "01 OBLIGACIONES GENERALES",
            "subcarpetas": {
                "laboratorio": "OBLIGACIÓN 2,5,6,9,13/ANEXO LABORATORIO",
                "comunicados_emitidos": "OBLIGACIÓN 7 y 10 / COMUNICADOS EMITIDOS",
                "comunicados_recibidos": "OBLIGACIÓN 7 y 10 / COMUNICADOS RECIBIDOS"
            }
        }

def get_nombre_carpeta_sharepoint(anio: int, mes: int) -> str:
    """
    Obtiene el nombre de carpeta de SharePoint desde el archivo de configuración JSON
    
    Primero busca en el archivo JSON. Si no encuentra, calcula dinámicamente como fallback.
    
    Args:
        anio: Año del informe
        mes: Mes del informe (1-12)
        
    Returns:
        Nombre de carpeta en formato SharePoint (ej: "11. 01SEP - 30SEP")
    """
    # Cargar configuración
    config_carpetas = _cargar_config_carpetas_sharepoint()
    
    # Buscar en la configuración
    for carpeta in config_carpetas.get("carpetas_periodo", []):
        if carpeta.get("anio") == anio and carpeta.get("mes") == mes:
            nombre_carpeta = carpeta.get("nombre_carpeta")
            if nombre_carpeta:
                logger.info(f"Carpeta encontrada en configuración: {nombre_carpeta} para {anio}-{mes}")
                return nombre_carpeta
    
    # Fallback: calcular dinámicamente si no está en la configuración
    logger.warning(f"No se encontró carpeta en configuración para {anio}-{mes}, calculando dinámicamente...")
    from calendar import monthrange
    
    # Calcular el número de carpeta (mes + 2)
    numero_carpeta = mes + 2
    
    # Obtener mes abreviado (primeras 3 letras en mayúsculas)
    mes_abrev = MESES[mes].upper()[:3]
    
    # Calcular el último día del mes
    ultimo_dia = monthrange(anio, mes)[1]
    
    # Formatear: "{numero}. 01{MES} - {ultimo_dia}{MES}"
    return f"{numero_carpeta}. 01{mes_abrev} - {ultimo_dia}{mes_abrev}"

def get_ruta_completa_sharepoint(anio: int, mes: int, tipo: str = "laboratorio") -> str:
    """
    Obtiene la ruta completa de SharePoint según el tipo de carpeta
    
    Args:
        anio: Año del informe
        mes: Mes del informe (1-12)
        tipo: Tipo de carpeta ("laboratorio", "comunicados_emitidos", "comunicados_recibidos")
        
    Returns:
        Ruta completa en formato SharePoint
    """
    # Obtener nombre de carpeta del periodo
    nombre_carpeta = get_nombre_carpeta_sharepoint(anio, mes)
    
    # Cargar configuración
    config_carpetas = _cargar_config_carpetas_sharepoint()
    
    # Obtener ruta base
    ruta_base = config_carpetas.get("ruta_base", "01 OBLIGACIONES GENERALES")
    
    # Obtener subcarpeta según el tipo
    subcarpetas = config_carpetas.get("subcarpetas", {})
    subcarpeta = subcarpetas.get(tipo, "")
    
    if subcarpeta:
        return f"{nombre_carpeta}/{ruta_base}/{subcarpeta}"
    else:
        return f"{nombre_carpeta}/{ruta_base}"

# ============================================================================
# CONFIGURACIÓN ADICIONAL
# ============================================================================

# Configuración OpenAI (LLM)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Configuración SharePoint (solo App Registration - username/password deprecado)
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL", "")
SHAREPOINT_CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID", "")
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
# Tenant ID de Azure AD (GUID) - Si no se proporciona, se extrae del dominio de SHAREPOINT_SITE_URL
SHAREPOINT_TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID", "")
# Ruta base adicional en SharePoint (ej: "Documentos compartidos" o "Shared Documents" o carpeta base)
SHAREPOINT_BASE_PATH = os.getenv("SHAREPOINT_BASE_PATH", "")

# Configuración GLPI MySQL
GLPI_MYSQL_HOST = os.getenv("GLPI_MYSQL_HOST", "")
GLPI_MYSQL_PORT = int(os.getenv("GLPI_MYSQL_PORT", "3306"))
GLPI_MYSQL_USER = os.getenv("GLPI_MYSQL_USER", "")
GLPI_MYSQL_PASSWORD = os.getenv("GLPI_MYSQL_PASSWORD", "")
GLPI_MYSQL_DATABASE = os.getenv("GLPI_MYSQL_DATABASE", "glpi")

# Lista de meses en español (para compatibilidad)
MESES_LISTA = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

