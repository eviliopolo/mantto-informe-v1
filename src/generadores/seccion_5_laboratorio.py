"""
Generador Sección 5: Informe de Laboratorio
Tipo: 🟩 GENERACIÓN PROGRAMÁTICA (python-docx)

Subsecciones:
- 5.1 Actividades Generales del Laboratorio
  - 5.1.1 Equipos Reintegrados al Inventario
  - 5.1.2 Equipos con Concepto de No Operatividad
  - 5.1.3 Equipos en Proceso de Garantía (RMA)
- 5.2 Equipos Pendientes por Repuestos
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from .base import GeneradorSeccion
import config


class GeneradorSeccion5(GeneradorSeccion):
    """Genera la Sección 5: Informe de Laboratorio usando python-docx"""
    
    # Colores corporativos
    COLOR_AZUL_OSCURO = RGBColor(31, 78, 121)   # Encabezados tabla equipos reparados
    COLOR_AZUL_MEDIO = RGBColor(46, 117, 182)   # Títulos de subsecciones
    COLOR_GRIS = RGBColor(64, 64, 64)           # Subtítulos
    COLOR_ROJO = RGBColor(192, 0, 0)            # Tabla equipos no operativos
    COLOR_AMARILLO = RGBColor(255, 165, 0)       # Tabla equipos en RMA
    
    @property
    def nombre_seccion(self) -> str:
        return "5. INFORME DE LABORATORIO"
    
    @property
    def template_file(self) -> str:
        return "seccion_5_laboratorio.docx"  # No se usa, pero debe existir para compatibilidad
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.datos: Dict[str, Any] = {}
        self.doc: Optional[Document] = None
    
    def cargar_datos(self) -> None:
        """Carga los datos de la sección 5 desde JSON"""
        archivo = config.FUENTES_DIR / f"laboratorio_{self.mes}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    self.datos = json.load(f)
            except Exception as e:
                print(f"[WARNING] Error al cargar datos desde {archivo}: {e}")
                self.datos = self._datos_ejemplo()
        else:
            print(f"[WARNING] Archivo de datos no encontrado: {archivo}")
            self.datos = self._datos_ejemplo()
        
        # Agregar mes y año si no están
        if 'mes' not in self.datos:
            self.datos['mes'] = config.MESES[self.mes]
        if 'anio' not in self.datos:
            self.datos['anio'] = self.anio
    
    def _datos_ejemplo(self) -> Dict[str, Any]:
        """Retorna datos de ejemplo para desarrollo"""
        return {
            "mes": config.MESES[self.mes],
            "anio": self.anio,
            "estadisticas": {
                "equipos_recibidos": 15,
                "equipos_reparados": 8,
                "equipos_no_reparables": 3,
                "equipos_rma": 4
            },
            "equipos_reparados": [
                {
                    "tipo_equipo": "Cámara PTZ Domo",
                    "serial": "CAM-PTZ-2023-0145",
                    "diagnostico": "Motor de pan/tilt averiado",
                    "reparacion": "Reemplazo motor completo y calibración",
                    "fecha_ingreso": "05/09/2024",
                    "fecha_salida": "18/09/2024"
                },
                {
                    "tipo_equipo": "Cámara IP 4MP",
                    "serial": "CAM-2023-0789",
                    "diagnostico": "Falla en fuente de poder",
                    "reparacion": "Reemplazo de fuente y verificación de voltaje",
                    "fecha_ingreso": "08/09/2024",
                    "fecha_salida": "15/09/2024"
                }
            ],
            "equipos_no_operativos": [
                {
                    "tipo_equipo": "Cámara PTZ Bullet",
                    "serial": "CAM-2019-0234",
                    "diagnostico": "Placa principal quemada",
                    "justificacion": "Daño irreversible, costo > 80% del equipo nuevo",
                    "fecha_concepto": "12/09/2024"
                }
            ],
            "equipos_rma_proceso": [
                {
                    "tipo_equipo": "Cámara IP 8MP",
                    "serial": "CAM-2023-0789",
                    "fabricante": "Hikvision",
                    "fecha_solicitud": "02/09/2024",
                    "estado_tramite": "Aprobado - Esperando reposición",
                    "dias_espera": 28
                }
            ],
            "equipos_pendientes_parte": [
                {
                    "tipo_equipo": "Cámara PTZ Exterior",
                    "serial": "CAM-2023-0345",
                    "parte_requerida": "Motor de pan/tilt completo",
                    "fecha_solicitud": "10/09/2024",
                    "estado_gestion": "En proceso de compra"
                }
            ],
            "resumen_partes_requeridas": [
                {
                    "parte": "Motor de pan/tilt",
                    "cantidad": 1,
                    "estado": "En proceso de compra"
                }
            ]
        }
    
    def _configurar_estilos(self):
        """Configura los estilos del documento"""
        if self.doc is None:
            return
        
        # Configurar márgenes (1.27 cm = 0.5 pulgadas)
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Cm(1.27)
            section.bottom_margin = Cm(1.27)
            section.left_margin = Cm(1.27)
            section.right_margin = Cm(1.27)
        
        # Estilo normal
        style = self.doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        
        # Título Sección (5.)
        h1 = self.doc.styles['Heading 1']
        h1.font.name = 'Arial'
        h1.font.size = Pt(14)
        h1.font.bold = True
        h1.font.color.rgb = self.COLOR_AZUL_OSCURO
        
        # Subsecciones (5.1, 5.2)
        h2 = self.doc.styles['Heading 2']
        h2.font.name = 'Arial'
        h2.font.size = Pt(12)
        h2.font.bold = True
        h2.font.color.rgb = self.COLOR_AZUL_MEDIO
        
        # Subtítulos (5.1.1, 5.1.2, etc.)
        h3 = self.doc.styles['Heading 3']
        h3.font.name = 'Arial'
        h3.font.size = Pt(11)
        h3.font.bold = True
        h3.font.color.rgb = self.COLOR_GRIS
    
    def _aplicar_sombreado_celda(self, cell, color: RGBColor):
        """
        Aplica color de fondo a celda de tabla
        RGBColor es una tupla (r, g, b) que se puede acceder con índices
        """
        shading_elm = OxmlElement('w:shd')
        # RGBColor es una tupla, acceder con índices
        r = color[0]
        g = color[1]
        b = color[2]
        
        hex_color = f'{r:02X}{g:02X}{b:02X}'
        shading_elm.set(qn('w:fill'), hex_color)
        cell._element.get_or_add_tcPr().append(shading_elm)
    
    def _centrar_celda_vertical(self, cell):
        """Centra verticalmente el contenido de una celda"""
        tc = cell._element
        tcPr = tc.get_or_add_tcPr()
        vAlign = OxmlElement('w:vAlign')
        vAlign.set(qn('w:val'), 'center')
        tcPr.append(vAlign)
    
    def _agregar_parrafo(self, texto: str, justificado: bool = True, negrita: bool = False, 
                        tamano: int = 11):
        """Agrega un párrafo de texto"""
        p = self.doc.add_paragraph()
        run = p.add_run(texto)
        run.bold = negrita
        run.font.name = 'Arial'
        run.font.size = Pt(tamano)
        if justificado:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        return p
    
    def _agregar_titulo_seccion(self):
        """Título principal: 5. INFORME DE LABORATORIO"""
        self.doc.add_heading("5. INFORME DE LABORATORIO", level=1)
    
    def _agregar_introduccion(self):
        """Párrafo introductorio de la sección"""
        mes = self.datos.get('mes', config.MESES[self.mes])
        anio = self.datos.get('anio', self.anio)
        
        texto = (
            f"Durante el mes de {mes} de {anio}, el laboratorio técnico ha realizado "
            f"actividades de diagnóstico, reparación y soporte técnico especializado "
            f"para los equipos de la red de videovigilancia. A continuación se presenta "
            f"el detalle de las actividades ejecutadas y el estado de los equipos en proceso."
        )
        self._agregar_parrafo(texto)
    
    def _agregar_5_1_actividades_generales(self):
        """Subsección 5.1 completa"""
        self.doc.add_heading("5.1. ACTIVIDADES GENERALES DEL LABORATORIO", level=2)
        
        # Párrafo introductorio
        estadisticas = self.datos.get('estadisticas', {})
        equipos_recibidos = estadisticas.get('equipos_recibidos', 0)
        equipos_reparados = estadisticas.get('equipos_reparados', 0)
        equipos_no_reparables = estadisticas.get('equipos_no_reparables', 0)
        equipos_rma = estadisticas.get('equipos_rma', 0)
        
        texto = (
            f"Durante el periodo reportado, el laboratorio recibió un total de "
            f"{equipos_recibidos} equipos para diagnóstico y reparación, de los cuales "
            f"{equipos_reparados} fueron reparados exitosamente y reintegrados al inventario "
            f"operativo. Se identificaron {equipos_no_reparables} equipos como no reparables "
            f"que requieren reposición, y {equipos_rma} equipos fueron gestionados bajo "
            f"proceso de garantía (RMA) con los fabricantes."
        )
        self._agregar_parrafo(texto)
        self.doc.add_paragraph()  # Espacio
        
        # Subsecciones
        self._agregar_5_1_1_reintegrados()
        self._agregar_5_1_2_no_operativos()
        self._agregar_5_1_3_rma()
    
    def _agregar_5_1_1_reintegrados(self):
        """Equipos reintegrados al inventario"""
        self.doc.add_heading("5.1.1. Equipos Reintegrados al Inventario", level=3)
        
        equipos = self.datos.get('equipos_reparados', [])
        
        if not equipos:
            self._agregar_parrafo(
                "No se registraron equipos reintegrados durante este periodo."
            )
            return
        
        self._agregar_parrafo(
            "Los siguientes equipos fueron diagnosticados, reparados y reintegrados "
            "al inventario disponible para su instalación en campo:"
        )
        self.doc.add_paragraph()  # Espacio
        
        self._crear_tabla_equipos_reparados(equipos)
    
    def _agregar_5_1_2_no_operativos(self):
        """Equipos con concepto de no operatividad"""
        self.doc.add_heading("5.1.2. Equipos con Concepto de No Operatividad", level=3)
        
        equipos = self.datos.get('equipos_no_operativos', [])
        
        if not equipos:
            self._agregar_parrafo(
                "No se registraron equipos con concepto de no operatividad durante este periodo."
            )
            return
        
        self._agregar_parrafo(
            "Los siguientes equipos fueron diagnosticados como no reparables debido a "
            "daños irreversibles en componentes críticos, obsolescencia tecnológica o "
            "costo de reparación superior al valor del equipo:"
        )
        self.doc.add_paragraph()  # Espacio
        
        self._crear_tabla_equipos_no_operativos(equipos)
    
    def _agregar_5_1_3_rma(self):
        """Equipos en proceso de garantía"""
        self.doc.add_heading("5.1.3. Equipos en Proceso de Garantía (RMA)", level=3)
        
        equipos = self.datos.get('equipos_rma_proceso', [])
        
        if not equipos:
            self._agregar_parrafo(
                "No se registraron equipos en proceso de garantía (RMA) durante este periodo."
            )
            return
        
        self._agregar_parrafo(
            "Los siguientes equipos se encuentran bajo proceso de garantía con los "
            "fabricantes, esperando autorización de RMA, reposición o reparación por "
            "parte del proveedor:"
        )
        self.doc.add_paragraph()  # Espacio
        
        self._crear_tabla_equipos_rma(equipos)
    
    def _agregar_5_2_pendiente_por_parte(self):
        """Equipos pendientes por repuestos"""
        self.doc.add_heading("5.2. EQUIPOS PENDIENTES POR REPUESTOS", level=2)
        
        equipos = self.datos.get('equipos_pendientes_parte', [])
        
        if not equipos:
            self._agregar_parrafo(
                "No se registraron equipos pendientes por repuestos durante este periodo."
            )
            return
        
        self._agregar_parrafo(
            "Los siguientes equipos se encuentran en espera de repuestos o partes "
            "específicas para completar su reparación. Se detalla el estado de gestión "
            "de cada componente requerido:"
        )
        self.doc.add_paragraph()  # Espacio
        
        self._crear_tabla_pendientes_parte(equipos)
        
        # Tabla resumen de partes
        resumen = self.datos.get('resumen_partes_requeridas', [])
        if resumen:
            self.doc.add_paragraph()  # Espacio
            self._agregar_parrafo("Resumen de partes requeridas:", negrita=True)
            self._crear_resumen_partes_requeridas(resumen)
    
    def _crear_tabla_equipos_reparados(self, equipos: List[Dict]):
        """Tabla 5.1.1 - Equipos Reintegrados"""
        encabezados = [
            "Tipo de Equipo", "Serial", "Diagnóstico", 
            "Reparación Realizada", "Fecha Ingreso", "Fecha Salida"
        ]
        anchos = [Cm(3.5), Cm(3.0), Cm(4.0), Cm(4.0), Cm(2.5), Cm(2.5)]
        
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            self._aplicar_sombreado_celda(hdr_cells[i], self.COLOR_AZUL_OSCURO)
            self._centrar_celda_vertical(hdr_cells[i])
        
        # Filas de datos
        for equipo in equipos:
            row_cells = tabla.add_row().cells
            fila = [
                equipo.get('tipo_equipo', ''),
                equipo.get('serial', ''),
                equipo.get('diagnostico', ''),
                equipo.get('reparacion', ''),
                equipo.get('fecha_ingreso', ''),
                equipo.get('fecha_salida', '')
            ]
            
            for i, texto in enumerate(fila):
                row_cells[i].text = str(texto) if texto else ""
                for paragraph in row_cells[i].paragraphs:
                    alineacion = WD_ALIGN_PARAGRAPH.CENTER if i >= 4 else WD_ALIGN_PARAGRAPH.LEFT
                    paragraph.alignment = alineacion
                    for run in paragraph.runs:
                        run.font.size = Pt(9)
                self._centrar_celda_vertical(row_cells[i])
        
        # Ajustar anchos
        for i, ancho in enumerate(anchos):
            for cell in tabla.columns[i].cells:
                cell.width = ancho
        
        self.doc.add_paragraph()
    
    def _crear_tabla_equipos_no_operativos(self, equipos: List[Dict]):
        """Tabla 5.1.2 - Equipos No Operativos"""
        encabezados = [
            "Tipo de Equipo", "Serial", "Diagnóstico",
            "Justificación No Reparable", "Fecha Concepto"
        ]
        anchos = [Cm(3.0), Cm(3.0), Cm(4.5), Cm(5.0), Cm(2.5)]
        
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            self._aplicar_sombreado_celda(hdr_cells[i], self.COLOR_ROJO)
            self._centrar_celda_vertical(hdr_cells[i])
        
        # Filas de datos
        for equipo in equipos:
            row_cells = tabla.add_row().cells
            fila = [
                equipo.get('tipo_equipo', ''),
                equipo.get('serial', ''),
                equipo.get('diagnostico', ''),
                equipo.get('justificacion', ''),
                equipo.get('fecha_concepto', '')
            ]
            
            for i, texto in enumerate(fila):
                row_cells[i].text = str(texto) if texto else ""
                for paragraph in row_cells[i].paragraphs:
                    alineacion = WD_ALIGN_PARAGRAPH.CENTER if i == 4 else WD_ALIGN_PARAGRAPH.LEFT
                    paragraph.alignment = alineacion
                    for run in paragraph.runs:
                        run.font.size = Pt(9)
                self._centrar_celda_vertical(row_cells[i])
        
        # Ajustar anchos
        for i, ancho in enumerate(anchos):
            for cell in tabla.columns[i].cells:
                cell.width = ancho
        
        self.doc.add_paragraph()
    
    def _crear_tabla_equipos_rma(self, equipos: List[Dict]):
        """Tabla 5.1.3 - Equipos en RMA"""
        encabezados = [
            "Tipo de Equipo", "Serial", "Fabricante",
            "Fecha Solicitud RMA", "Estado Trámite", "Tiempo Esperando (días)"
        ]
        anchos = [Cm(3.0), Cm(2.8), Cm(2.8), Cm(2.5), Cm(3.5), Cm(2.4)]
        
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0, 0, 0)  # Negro para fondo amarillo
            self._aplicar_sombreado_celda(hdr_cells[i], self.COLOR_AMARILLO)
            self._centrar_celda_vertical(hdr_cells[i])
        
        # Filas de datos
        for equipo in equipos:
            row_cells = tabla.add_row().cells
            fila = [
                equipo.get('tipo_equipo', ''),
                equipo.get('serial', ''),
                equipo.get('fabricante', ''),
                equipo.get('fecha_solicitud', ''),
                equipo.get('estado_tramite', ''),
                str(equipo.get('dias_espera', ''))
            ]
            
            for i, texto in enumerate(fila):
                row_cells[i].text = str(texto) if texto else ""
                for paragraph in row_cells[i].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in paragraph.runs:
                        run.font.size = Pt(9)
                self._centrar_celda_vertical(row_cells[i])
        
        # Ajustar anchos
        for i, ancho in enumerate(anchos):
            for cell in tabla.columns[i].cells:
                cell.width = ancho
        
        self.doc.add_paragraph()
    
    def _crear_tabla_pendientes_parte(self, equipos: List[Dict]):
        """Tabla 5.2 - Equipos Pendientes por Repuestos"""
        encabezados = [
            "Tipo de Equipo", "Serial", "Parte/Repuesto Requerido",
            "Fecha Solicitud", "Estado de Gestión"
        ]
        anchos = [Cm(3.0), Cm(3.0), Cm(4.5), Cm(2.5), Cm(4.0)]
        
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            self._aplicar_sombreado_celda(hdr_cells[i], self.COLOR_AZUL_MEDIO)
            self._centrar_celda_vertical(hdr_cells[i])
        
        # Filas de datos
        for equipo in equipos:
            row_cells = tabla.add_row().cells
            fila = [
                equipo.get('tipo_equipo', ''),
                equipo.get('serial', ''),
                equipo.get('parte_requerida', ''),
                equipo.get('fecha_solicitud', ''),
                equipo.get('estado_gestion', '')
            ]
            
            for i, texto in enumerate(fila):
                row_cells[i].text = str(texto) if texto else ""
                for paragraph in row_cells[i].paragraphs:
                    alineacion = WD_ALIGN_PARAGRAPH.CENTER if i == 3 else WD_ALIGN_PARAGRAPH.LEFT
                    paragraph.alignment = alineacion
                    for run in paragraph.runs:
                        run.font.size = Pt(9)
                self._centrar_celda_vertical(row_cells[i])
        
        # Ajustar anchos
        for i, ancho in enumerate(anchos):
            for cell in tabla.columns[i].cells:
                cell.width = ancho
        
        self.doc.add_paragraph()
    
    def _crear_resumen_partes_requeridas(self, resumen: List[Dict]):
        """Tabla Resumen de Partes Requeridas"""
        encabezados = ["Repuesto/Parte", "Cantidad Requerida", "Estado"]
        anchos = [Cm(6.0), Cm(3.0), Cm(5.0)]
        
        tabla = self.doc.add_table(rows=1, cols=len(encabezados))
        tabla.style = 'Table Grid'
        tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Encabezados
        hdr_cells = tabla.rows[0].cells
        for i, texto in enumerate(encabezados):
            hdr_cells[i].text = texto
            for paragraph in hdr_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(255, 255, 255)
            self._aplicar_sombreado_celda(hdr_cells[i], self.COLOR_GRIS)
            self._centrar_celda_vertical(hdr_cells[i])
        
        # Filas de datos
        for parte in resumen:
            row_cells = tabla.add_row().cells
            fila = [
                parte.get('parte', ''),
                str(parte.get('cantidad', '')),
                parte.get('estado', '')
            ]
            
            for i, texto in enumerate(fila):
                row_cells[i].text = str(texto) if texto else ""
                for paragraph in row_cells[i].paragraphs:
                    alineacion = WD_ALIGN_PARAGRAPH.CENTER if i == 1 else WD_ALIGN_PARAGRAPH.LEFT
                    paragraph.alignment = alineacion
                    for run in paragraph.runs:
                        run.font.size = Pt(9)
                self._centrar_celda_vertical(row_cells[i])
        
        # Ajustar anchos
        for i, ancho in enumerate(anchos):
            for cell in tabla.columns[i].cells:
                cell.width = ancho
        
        self.doc.add_paragraph()
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa los datos y retorna el contexto (no se usa en generación programática)"""
        return {}
    
    def generar(self) -> Document:
        """
        Genera el documento completo de la Sección 5
        Sobrescribe el método de la clase base para usar python-docx directamente
        """
        # Cargar datos si no se han cargado
        if not self.datos:
            self.cargar_datos()
        
        # Crear documento
        self.doc = Document()
        self._configurar_estilos()
        
        # Generar contenido
        self._agregar_titulo_seccion()
        self._agregar_introduccion()
        self._agregar_5_1_actividades_generales()
        self._agregar_5_2_pendiente_por_parte()
        
        # Separador fin de sección
        self.doc.add_paragraph()
        p = self.doc.add_paragraph("═" * 60)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        p = self.doc.add_paragraph("Fin Sección 5 - Informe de Laboratorio")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True
        p.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        return self.doc
    
    def guardar(self, output_path: Path) -> None:
        """
        Genera y guarda la sección
        Sobrescribe el método de la clase base para usar python-docx
        """
        if self.doc is None:
            self.generar()
        
        self.doc.save(str(output_path))
        print(f"[OK] {self.nombre_seccion} guardada en: {output_path}")
