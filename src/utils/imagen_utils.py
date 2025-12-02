"""
Utilidades para procesamiento de imágenes en documentos Word
"""
from typing import Optional
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import base64
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


def base64_to_inline_image(template: DocxTemplate, base64_str: str, width_mm: int = 150) -> Optional[InlineImage]:
    """
    Convierte una imagen en formato base64 a InlineImage para usar en docxtpl.
    
    Args:
        template: Template de docxtpl
        base64_str: String base64 de la imagen (puede incluir prefijo data:image/...)
        width_mm: Ancho de la imagen en milímetros (por defecto 150)
        
    Returns:
        InlineImage o None si falla
    """
    if not base64_str or not isinstance(base64_str, str):
        return None

    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    # Decodificar
    try:
        image_bytes = base64.b64decode(base64_str)
    except Exception as e:
        logger.warning(f"Error al decodificar base64: {e}")
        return None

    # Crear imagen en memoria
    stream = BytesIO(image_bytes)

    # Validar imagen opcionalmente
    try:
        Image.open(stream)
        stream.seek(0)  # Resetear el stream después de validar
    except Exception as e:
        logger.warning(f"La imagen Base64 no es válida: {e}")
        return None

    # Crear InlineImage
    try:
        return InlineImage(template, stream, width=Mm(width_mm))
    except Exception as e:
        logger.warning(f"Error al crear InlineImage: {e}")
        return None


def procesar_imagen(template: DocxTemplate, image_b64: str) -> Optional[InlineImage]:
    """
    Convierte una imagen base64 a InlineImage o retorna None si falla.
    Wrapper simplificado de base64_to_inline_image.
    
    Args:
        image_b64: String base64 de la imagen
        
    Returns:
        InlineImage o None si falla
    """
    if template and image_b64:
        try:
            return base64_to_inline_image(template, image_b64)
        except Exception as e:
            logger.warning(f"Error procesando imagen: {e}")
            return None
    return None

