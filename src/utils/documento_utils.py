"""
Utilidades para manipulación de documentos Word y URLs de SharePoint
"""
from pathlib import Path
from typing import List
from docx import Document
from urllib.parse import urlparse, unquote

def combinar_documentos(archivos: List[Path], archivo_salida: Path) -> None:
    """
    Combina múltiples documentos Word en uno solo
    
    Args:
        archivos: Lista de rutas a los documentos a combinar
        archivo_salida: Ruta del archivo de salida
    """
    if not archivos:
        raise ValueError("No hay documentos para combinar")
    
    documento_final = Document(archivos[0])
    
    # Agregar cada documento subsecuente
    for archivo in archivos[1:]:
        doc_temp = Document(archivo)
        
        # Agregar salto de página antes de cada nuevo documento (excepto el primero)
        documento_final.add_page_break()
        
        # Copiar elementos de cada sección
        for elemento in doc_temp.element.body:
            documento_final.element.body.append(elemento)
    
    documento_final.save(str(archivo_salida))

def agregar_pagina_nueva(doc: Document) -> None:
    """
    Agrega un salto de página al documento
    
    Args:
        doc: Documento Word
    """
    doc.add_page_break()

def aplicar_estilo_titulo(parrafo, nivel: int = 1) -> None:
    """
    Aplica estilo de título a un párrafo
    
    Args:
        parrafo: Párrafo del documento
        nivel: Nivel del título (1-9)
    """
    estilo = f"Heading {min(nivel, 9)}"
    parrafo.style = estilo


def convertir_url_sharepoint_a_ruta_relativa(url_completa: str) -> str:
    """
    Convierte una URL completa de SharePoint a ruta relativa del servidor.
    
    Args:
        url_completa: URL completa de SharePoint (ej: https://...)
        
    Returns:
        Ruta relativa del servidor (ej: /sites/OPERACIONES/Shared Documents/...)
    """
    if not url_completa.startswith("http://") and not url_completa.startswith("https://"):
        # Ya es una ruta relativa, retornarla tal cual
        return url_completa
    
    # Parsear la URL y decodificar los caracteres codificados
    url_parsed = urlparse(url_completa)
    # Decodificar el path para obtener los caracteres reales (ej: %20 -> espacio, %C3%B1o -> año)
    path_decodificado = unquote(url_parsed.path)
    path_parts = [p for p in path_decodificado.split('/') if p]  # Eliminar vacíos
    
    # Encontrar el índice de 'sites', 'teams' o 'personal'
    try:
        idx = next(i for i, part in enumerate(path_parts) if part in ['sites', 'teams', 'personal'])
        # Construir ruta relativa: /sites/... o /teams/... o /personal/...
        server_relative_url = '/' + '/'.join(path_parts[idx:])
        return server_relative_url
    except StopIteration:
        # Si no encuentra, usar toda la ruta después del dominio (ya decodificada)
        server_relative_url = path_decodificado if path_decodificado.startswith('/') else '/' + path_decodificado
        return server_relative_url


