"""
Generador Sección 13: Anexos
Tipo: 🟩 EXTRACCIÓN DATOS (listado de anexos del periodo)

Esta sección lista los anexos entregados durante el periodo del informe,
incluyendo actas, evidencias fotográficas, reportes técnicos y documentos complementarios.
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
from .base import GeneradorSeccion
import config


class GeneradorSeccion13(GeneradorSeccion):
    """Genera la sección 13: Anexos"""
    
    @property
    def nombre_seccion(self) -> str:
        return "13. ANEXOS"
    
    @property
    def template_file(self) -> str:
        return "seccion_13_anexos.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.anexos: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 13 desde CSV o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "anexos.csv"
        
        datos_cargados = False
        
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
                # Convertir DataFrame a lista de diccionarios
                self.anexos = df.to_dict('records')
                datos_cargados = True
                print(f"[INFO] Datos cargados desde CSV: {archivo_csv}")
            except Exception as e:
                print(f"[WARNING] Error al cargar CSV {archivo_csv}: {e}")
        
        # Si no hay datos, generar dummy
        if not datos_cargados:
            print(f"[INFO] No se encontraron fuentes de datos, generando datos dummy para pruebas")
            self._generar_datos_dummy()
            self._guardar_csv_demo()
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        self.anexos = [
            {
                "nombre": "Acta de mantenimiento consolidado del mes",
                "tipo": "PDF",
                "ruta": "{{ ruta_acta_pdf }}"
            },
            {
                "nombre": "Evidencias fotográficas de intervenciones",
                "tipo": "IMAGENES",
                "ruta": "{{ carpeta_fotos }}"
            },
            {
                "nombre": "Reporte técnico de incidentes",
                "tipo": "PDF",
                "ruta": "{{ reporte_incidentes_pdf }}"
            },
            {
                "nombre": f"Listado de equipos intervenidos - {mes_nombre} {self.anio}",
                "tipo": "EXCEL",
                "ruta": "{{ listado_equipos_xlsx }}"
            },
            {
                "nombre": "Actas de inspección de seguridad",
                "tipo": "PDF",
                "ruta": "{{ actas_inspeccion_pdf }}"
            },
            {
                "nombre": "Evidencias de capacitaciones realizadas",
                "tipo": "IMAGENES",
                "ruta": "{{ evidencias_capacitaciones }}"
            },
            {
                "nombre": "Reporte de ejecución presupuestal detallado",
                "tipo": "EXCEL",
                "ruta": "{{ reporte_presupuestal_xlsx }}"
            },
            {
                "nombre": "Matriz de riesgos actualizada",
                "tipo": "PDF",
                "ruta": "{{ matriz_riesgos_pdf }}"
            },
            {
                "nombre": "Comunicados emitidos y recibidos",
                "tipo": "PDF",
                "ruta": "{{ comunicados_pdf }}"
            },
            {
                "nombre": "Soportes de entrega de EPP",
                "tipo": "PDF",
                "ruta": "{{ soportes_epp_pdf }}"
            }
        ]
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            df = pd.DataFrame(self.anexos)
            csv_demo = config.FUENTES_DIR / "anexos_demo.csv"
            df.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Anexos
            "anexos": self.anexos,
            "total_anexos": len(self.anexos),
            "hay_anexos": len(self.anexos) > 0,
        }

