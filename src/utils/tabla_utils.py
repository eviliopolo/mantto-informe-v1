"""
Utilidades para crear tablas en documentos Word
"""
from typing import List, Dict, Any
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import logging

logger = logging.getLogger(__name__)

def crear_tabla_desde_dict(doc: Document, datos: List[Dict[str, Any]], encabezados: List[str]) -> None:
    """
    Crea una tabla en un documento Word a partir de una lista de diccionarios
    
    Args:
        doc: Documento Word
        datos: Lista de diccionarios con los datos
        encabezados: Lista de nombres de columnas
    """
    if not datos:
        return
    
    # Crear tabla
    tabla = doc.add_table(rows=1, cols=len(encabezados))
    tabla.style = 'Light Grid Accent 1'
    
    # Agregar encabezados
    header_cells = tabla.rows[0].cells
    for i, encabezado in enumerate(encabezados):
        header_cells[i].text = encabezado
        header_cells[i].paragraphs[0].runs[0].bold = True
        header_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Agregar datos
    for fila_datos in datos:
        row_cells = tabla.add_row().cells
        for i, encabezado in enumerate(encabezados):
            valor = fila_datos.get(encabezado, "")
            row_cells[i].text = str(valor) if valor is not None else ""
    
    return tabla

def crear_tabla_desde_lista(doc: Document, datos: List[List[Any]], encabezados: List[str] = None) -> None:
    """
    Crea una tabla en un documento Word a partir de una lista de listas
    
    Args:
        doc: Documento Word
        datos: Lista de listas con los datos (cada lista es una fila)
        encabezados: Lista opcional de nombres de columnas
    """
    if not datos:
        return
    
    num_cols = len(datos[0]) if datos else len(encabezados) if encabezados else 0
    if num_cols == 0:
        return
    
    # Crear tabla
    num_rows = len(datos) + (1 if encabezados else 0)
    tabla = doc.add_table(rows=num_rows, cols=num_cols)
    tabla.style = 'Light Grid Accent 1'
    
    # Agregar encabezados si existen
    if encabezados:
        header_cells = tabla.rows[0].cells
        for i, encabezado in enumerate(encabezados):
            header_cells[i].text = str(encabezado)
            header_cells[i].paragraphs[0].runs[0].bold = True
            header_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        inicio_datos = 1
    else:
        inicio_datos = 0
    
    # Agregar datos
    for idx, fila_datos in enumerate(datos):
        row_cells = tabla.rows[inicio_datos + idx].cells
        for i, valor in enumerate(fila_datos):
            row_cells[i].text = str(valor) if valor is not None else ""
    
    return tabla


def set_cell_shading(cell, hex_color: str):
    """Aplica color de fondo a una celda de tabla"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), hex_color)
    cell._element.get_or_add_tcPr().append(shading_elm)


def centrar_celda_vertical(cell):
    """Centra verticalmente el contenido de una celda"""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), 'center')
    tcPr.append(vAlign)


def enable_autofit(table):
    """Activa el autoajuste para tablas en Word"""
    tbl = table._element
    if tbl.tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    else:
        tblPr = tbl.tblPr
    tblLayout = tblPr.find(qn('w:tblLayout'))
    if tblLayout is not None:
        tblPr.remove(tblLayout)
    new_tblLayout = OxmlElement('w:tblLayout')
    new_tblLayout.set(qn('w:type'), 'autofit')
    tblPr.append(new_tblLayout)
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None:
        tblPr.remove(tblW)


def habilitar_encabezado_repetido(table, num_filas: int = 1):
    """
    Habilita que el encabezado de la tabla se repita en cada página cuando hay un salto de página.
    
    Args:
        table: Tabla de Word
        num_filas: Número de filas a marcar como encabezado (por defecto 1, la primera fila)
    """
    if num_filas < 1 or num_filas > len(table.rows):
        num_filas = 1
    
    for i in range(num_filas):
        row = table.rows[i]
        tr = row._element  # Elemento XML de la fila
        
        # Obtener o crear trPr (propiedades de la fila)
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr')
            tr.insert(0, trPr)
        
        # Buscar si ya existe tblHeader
        tblHeader = trPr.find(qn('w:tblHeader'))
        if tblHeader is None:
            # Crear el elemento tblHeader
            tblHeader = OxmlElement('w:tblHeader')
            trPr.append(tblHeader)
        
        # Establecer el valor a 'true' (aunque el elemento solo necesita existir)
        tblHeader.set(qn('w:val'), 'true')


def detectar_columnas_desde_datos(datos: List[Dict[str, Any]]) -> tuple[List[str], List[str]]:
    """Detecta automáticamente los headers y campos desde los datos"""
    if not datos:
        return [], []
    campos = list(datos[0].keys())
    headers = [campo.replace("_", " ").upper() for campo in campos]
    return headers, campos


def preparar_datos_tabla(datos: List[Dict[str, Any]], headers: List[str], campos: List[str], 
                          agregar_totales: bool = False, columna_total_texto: int = 0) -> List[List[str]]:
    """Prepara los datos de una tabla en formato lista de listas"""
    table_data = [headers]
    for item in datos:
        fila = []
        for campo in campos:
            valor = item.get(campo, "")
            fila.append(str(valor) if valor is not None else "")
        table_data.append(fila)
    if agregar_totales and datos:
        fila_total = []
        for idx, campo in enumerate(campos):
            if idx == columna_total_texto:
                fila_total.append("TOTAL")
            else:
                try:
                    total = 0
                    for item in datos:
                        valor = item.get(campo, "")
                        if valor:
                            if isinstance(valor, str):
                                valor_limpio = valor.replace(",", "").replace(" ", "").strip()
                                if valor_limpio:
                                    total += float(valor_limpio)
                            else:
                                total += float(valor)
                    fila_total.append(str(int(total)) if total == int(total) else str(total))
                except (ValueError, TypeError):
                    fila_total.append("")
        table_data.append(fila_total)
    return table_data


def count_rows(table_data: List[List[str]]) -> int:
    """Cuenta el número de registros en una tabla preparada"""
    if not table_data or len(table_data) == 0:
        return 0
    count = len(table_data) - 1
    if len(table_data) > 1:
        ultima_fila = table_data[-1]
        if ultima_fila and len(ultima_fila) > 0:
            if str(ultima_fila[0]).upper() == "TOTAL":
                count -= 1
    return max(0, count)


def reemplazar_placeholder_con_tabla(doc: Document, placeholder: str, table_data: List[List[str]]):
    """Busca un placeholder y lo reemplaza con una tabla"""
    if not table_data or len(table_data) == 0:
        return
    estilos_tabla = ['Table Grid', 'Light Shading', 'Light List', 'Medium Shading 1', 'Light Grid']
    for i, paragraph in enumerate(doc.paragraphs):
        if placeholder in paragraph.text:
            tabla = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
            try:
                tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
            except:
                try:
                    tbl_pr = tabla._tbl.tblPr
                    if tbl_pr is None:
                        from docx.oxml import parse_xml
                        tbl_pr = parse_xml(r'<w:tblPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:jc w:val="center"/></w:tblPr>')
                        tabla._tbl.insert(0, tbl_pr)
                    else:
                        jc = tbl_pr.find(qn('w:jc'))
                        if jc is None:
                            jc = OxmlElement('w:jc')
                            jc.set(qn('w:val'), 'center')
                            tbl_pr.append(jc)
                        else:
                            jc.set(qn('w:val'), 'center')
                except Exception as e:
                    logger.warning(f"No se pudo centrar la tabla: {e}")
            estilo_aplicado = False
            for estilo in estilos_tabla:
                try:
                    tabla.style = estilo
                    estilo_aplicado = True
                    break
                except:
                    continue
            if not estilo_aplicado:
                try:
                    tabla.style = 'Table Grid'
                except:
                    pass
            enable_autofit(tabla)
            # Habilitar que el encabezado se repita en cada página
            habilitar_encabezado_repetido(tabla, num_filas=1)
            total_rows = len(table_data)
            for row_idx, fila in enumerate(table_data):
                for col_idx, valor in enumerate(fila):
                    celda = tabla.rows[row_idx].cells[col_idx]
                    celda.text = str(valor) if valor is not None else ""
                    if row_idx == 0:
                        set_cell_shading(celda, "1F4E79")
                        centrar_celda_vertical(celda)
                        for paragraph_celda in celda.paragraphs:
                            paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for run in paragraph_celda.runs:
                                run.bold = True
                                run.font.size = Pt(8)
                                run.font.color.rgb = RGBColor(255, 255, 255)
                    elif row_idx == total_rows - 1 and fila[0].upper() == "TOTAL":
                        set_cell_shading(celda, "D9E1F2")
                        centrar_celda_vertical(celda)
                        for paragraph_celda in celda.paragraphs:
                            paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for run in paragraph_celda.runs:
                                run.bold = True
                                run.font.size = Pt(8)
                                run.font.color.rgb = RGBColor(0, 0, 0)
                    else:
                        if row_idx % 2 == 0:
                            set_cell_shading(celda, "F2F2F2")
                        else:
                            set_cell_shading(celda, "FFFFFF")
                        centrar_celda_vertical(celda)
                        for paragraph_celda in celda.paragraphs:
                            if col_idx == 0:
                                paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            else:
                                paragraph_celda.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for run in paragraph_celda.runs:
                                run.font.size = Pt(8)
                                run.font.color.rgb = RGBColor(0, 0, 0)
            parent = paragraph._element.getparent()
            para_idx = parent.index(paragraph._element)
            parent.insert(para_idx + 1, tabla._element)
            paragraph.text = paragraph.text.replace(placeholder, "").strip()
            if not paragraph.text.strip():
                parent.remove(paragraph._element)
            break

