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

# Formatos de imagen soportados por python-docx
FORMATOS_SOPORTADOS = {'JPEG', 'PNG', 'GIF', 'BMP'}


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

    # Limpiar el string base64 si tiene prefijo data:image/...
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    # Decodificar
    try:
        image_bytes = base64.b64decode(base64_str)
    except Exception as e:
        logger.warning(f"Error al decodificar base64: {e}")
        return None

    if not image_bytes:
        logger.warning("Los bytes de la imagen están vacíos")
        return None

    # Validar y procesar la imagen
    try:
        # Crear un stream para validar la imagen
        validation_stream = BytesIO(image_bytes)
        pil_image = Image.open(validation_stream)
        
        # Verificar que el formato sea soportado por python-docx
        formato = pil_image.format
        if not formato or formato.upper() not in FORMATOS_SOPORTADOS:
            logger.warning(f"Formato de imagen no soportado: {formato}. Convirtiendo a PNG...")
            # Convertir a PNG si no es un formato soportado
            output_stream = BytesIO()
            # Convertir a RGB si es necesario (para formatos con transparencia)
            if pil_image.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', pil_image.size, (255, 255, 255))
                if pil_image.mode == 'P':
                    pil_image = pil_image.convert('RGBA')
                rgb_image.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode == 'RGBA' else None)
                pil_image = rgb_image
            pil_image.save(output_stream, format='PNG')
            output_stream.seek(0)
            final_stream = output_stream
        else:
            # Crear un nuevo stream limpio con los bytes originales
            final_stream = BytesIO(image_bytes)
            final_stream.seek(0)
        
        # Crear InlineImage con el stream validado
        return InlineImage(template, final_stream, width=Mm(width_mm))
        
    except Exception as e:
        logger.warning(f"Error al procesar imagen: {e}")
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

