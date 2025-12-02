"""
Utilidades para trabajar con informes aprobados
"""
from pathlib import Path
from typing import List, Optional
import config
import re

try:
    import PyPDF2
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

try:
    from docx import Document as DocxDocument
    DOCX_DISPONIBLE = True
except ImportError:
    DOCX_DISPONIBLE = False


def obtener_ultimos_informes_aprobados(cantidad: int = 3) -> List[Path]:
    """
    Obtiene los últimos N informes aprobados ordenados por fecha de modificación
    
    Args:
        cantidad: Número de informes a obtener (default: 3)
        
    Returns:
        Lista de Paths a los archivos de informes aprobados
    """
    if not config.INFORMES_APROBADOS_DIR.exists():
        print(f"[WARNING] Directorio de informes aprobados no existe: {config.INFORMES_APROBADOS_DIR}")
        return []
    
    # Obtener todos los archivos PDF y DOCX
    archivos = []
    for ext in ['*.pdf', '*.docx']:
        archivos.extend(config.INFORMES_APROBADOS_DIR.glob(ext))
    
    if not archivos:
        print(f"[WARNING] No se encontraron informes aprobados en {config.INFORMES_APROBADOS_DIR}")
        return []
    
    # Ordenar por fecha de modificación (más reciente primero)
    archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Retornar los últimos N
    return archivos[:cantidad]


def extraer_seccion_informe(ruta_informe: Path, numero_seccion: str, nombre_seccion: str, siguiente_seccion: Optional[str] = None) -> Optional[str]:
    """
    Extrae una sección específica de un informe aprobado
    
    Args:
        ruta_informe: Path al archivo del informe (PDF o DOCX)
        numero_seccion: Número de la sección (ej: "1.5.1", "1.5.2", "1.5.3")
        nombre_seccion: Nombre de la sección (ej: "OBLIGACIONES GENERALES", "OBLIGACIONES ESPECÍFICAS")
        siguiente_seccion: Número de la siguiente sección para delimitar el final (ej: "1.5.2", "1.6")
        
    Returns:
        Texto de la sección o None si no se encuentra
    """
    if not ruta_informe.exists():
        return None
    
    extension = ruta_informe.suffix.lower()
    texto_completo = ""
    
    try:
        if extension == '.pdf' and PDF_DISPONIBLE:
            with open(ruta_informe, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    texto_completo += page.extract_text() + "\n"
        elif extension in ['.docx', '.doc'] and DOCX_DISPONIBLE:
            doc = DocxDocument(ruta_informe)
            for para in doc.paragraphs:
                texto_completo += para.text + "\n"
        else:
            print(f"[WARNING] Formato no soportado para extracción: {extension}")
            return None
        
        # Escapar el número de sección para regex
        numero_escaped = re.escape(numero_seccion)
        
        # Buscar la sección con diferentes patrones
        patrones = [
            rf'{numero_escaped}[\.\s]+{re.escape(nombre_seccion)}',
            rf'{numero_escaped}[\.\s]+{nombre_seccion}',
        ]
        
        inicio_seccion = None
        for patron in patrones:
            match = re.search(patron, texto_completo, re.IGNORECASE)
            if match:
                inicio_seccion = match.start()
                break
        
        if inicio_seccion is None:
            print(f"[WARNING] No se encontró la sección {numero_seccion} ({nombre_seccion}) en {ruta_informe.name}")
            return None
        
        # Extraer desde el inicio de la sección hasta la siguiente sección
        texto_desde_seccion = texto_completo[inicio_seccion:]
        
        # Buscar el final de la sección
        fin_patrones = []
        if siguiente_seccion:
            siguiente_escaped = re.escape(siguiente_seccion)
            fin_patrones.append(rf'{siguiente_escaped}[\.\s]')
        
        # Patrones adicionales para detectar el final
        fin_patrones.extend([
            r'1\.6[\.\s]',
            r'2\.\s',
        ])
        
        fin_seccion = len(texto_desde_seccion)
        for patron in fin_patrones:
            match = re.search(patron, texto_desde_seccion, re.IGNORECASE)
            if match:
                fin_seccion = match.start()
                break
        
        seccion_texto = texto_desde_seccion[:fin_seccion].strip()
        
        if len(seccion_texto) < 100:
            print(f"[WARNING] Sección {numero_seccion} extraída es muy corta ({len(seccion_texto)} caracteres) en {ruta_informe.name}")
            return None
        
        print(f"[INFO] Sección {numero_seccion} ({nombre_seccion}) extraída de {ruta_informe.name}: {len(seccion_texto)} caracteres")
        return seccion_texto
        
    except Exception as e:
        print(f"[WARNING] Error al extraer sección {numero_seccion} de {ruta_informe.name}: {e}")
        return None


def extraer_seccion_obligaciones_generales(ruta_informe: Path) -> Optional[str]:
    """
    Extrae la sección 1.5.1 OBLIGACIONES GENERALES de un informe aprobado
    
    Args:
        ruta_informe: Path al archivo del informe (PDF o DOCX)
        
    Returns:
        Texto de la sección 1.5.1 o None si no se encuentra
    """
    return extraer_seccion_informe(
        ruta_informe, 
        "1.5.1", 
        "OBLIGACIONES GENERALES", 
        siguiente_seccion="1.5.2"
    )


def extraer_seccion_obligaciones_especificas(ruta_informe: Path) -> Optional[str]:
    """
    Extrae la sección 1.5.2 OBLIGACIONES ESPECÍFICAS DEL CONTRATISTA de un informe aprobado
    
    Args:
        ruta_informe: Path al archivo del informe (PDF o DOCX)
        
    Returns:
        Texto de la sección 1.5.2 o None si no se encuentra
    """
    return extraer_seccion_informe(
        ruta_informe, 
        "1.5.2", 
        "OBLIGACIONES ESPECÍFICAS", 
        siguiente_seccion="1.5.3"
    )


def extraer_seccion_obligaciones_ambientales(ruta_informe: Path) -> Optional[str]:
    """
    Extrae la sección 1.5.3 OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL de un informe aprobado
    
    Args:
        ruta_informe: Path al archivo del informe (PDF o DOCX)
        
    Returns:
        Texto de la sección 1.5.3 o None si no se encuentra
    """
    return extraer_seccion_informe(
        ruta_informe, 
        "1.5.3", 
        "OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL", 
        siguiente_seccion="1.5.4"
    )


def obtener_contexto_informes_aprobados(cantidad: int = 3, tipo_seccion: str = "generales") -> List[str]:
    """
    Obtiene el texto de una sección específica de los últimos N informes aprobados
    
    Args:
        cantidad: Número de informes a procesar (default: 3)
        tipo_seccion: Tipo de sección a extraer. Opciones:
                     - "generales" (1.5.1 OBLIGACIONES GENERALES)
                     - "especificas" (1.5.2 OBLIGACIONES ESPECÍFICAS)
                     - "ambientales" (1.5.3 OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL)
        
    Returns:
        Lista de textos de la sección especificada de cada informe
    """
    informes = obtener_ultimos_informes_aprobados(cantidad)
    contextos = []
    
    # Seleccionar función de extracción según el tipo de sección
    if tipo_seccion == "generales":
        funcion_extraccion = extraer_seccion_obligaciones_generales
        nombre_seccion = "1.5.1 OBLIGACIONES GENERALES"
    elif tipo_seccion == "especificas":
        funcion_extraccion = extraer_seccion_obligaciones_especificas
        nombre_seccion = "1.5.2 OBLIGACIONES ESPECÍFICAS"
    elif tipo_seccion == "ambientales":
        funcion_extraccion = extraer_seccion_obligaciones_ambientales
        nombre_seccion = "1.5.3 OBLIGACIONES ESPECÍFICAS EN MATERIA AMBIENTAL"
    else:
        print(f"[WARNING] Tipo de sección desconocido: {tipo_seccion}, usando 'generales' por defecto")
        funcion_extraccion = extraer_seccion_obligaciones_generales
        nombre_seccion = "1.5.1 OBLIGACIONES GENERALES"
    
    for informe in informes:
        texto_seccion = funcion_extraccion(informe)
        if texto_seccion:
            contextos.append(texto_seccion)
    
    print(f"[INFO] Se obtuvieron {len(contextos)} contextos de la sección {nombre_seccion} de informes aprobados")
    return contextos

