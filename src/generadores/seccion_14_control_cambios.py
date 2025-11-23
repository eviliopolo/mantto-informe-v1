"""
Generador Sección 14: Control de Revisiones y Cambios
Tipo: 🟩 EXTRACCIÓN DATOS (historial de versiones y cambios del documento)

Esta sección contiene el registro estructurado de versiones, fechas, responsables
y descripciones de cambios realizados en el informe mensual.
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
from .base import GeneradorSeccion
import config


class GeneradorSeccion14(GeneradorSeccion):
    """Genera la sección 14: Control de Revisiones y Cambios"""
    
    @property
    def nombre_seccion(self) -> str:
        return "14. CONTROL DE REVISIONES Y CAMBIOS"
    
    @property
    def template_file(self) -> str:
        return "seccion_14_control_cambios.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.cambios: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 14 desde CSV o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "control_cambios.csv"
        
        datos_cargados = False
        
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
                # Convertir DataFrame a lista de diccionarios
                self.cambios = df.to_dict('records')
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
        
        # Generar historial de cambios dummy
        # Incluir versiones desde el inicio del contrato hasta el mes actual
        self.cambios = [
            {
                "version": "1.0",
                "fecha": "2024-11-15",
                "responsable": "Coordinación Técnica",
                "descripcion": "Versión inicial del informe para el periodo de inicio del contrato.",
                "observaciones": "N/A"
            },
            {
                "version": "1.1",
                "fecha": "2024-12-20",
                "responsable": "Coordinación Operativa",
                "descripcion": "Actualización de cifras ANS y anexos según revisión ETB.",
                "observaciones": "Se ajustaron tablas según observaciones de la interventoría."
            },
            {
                "version": "1.2",
                "fecha": "2025-01-18",
                "responsable": "Coordinación Técnica",
                "descripcion": "Inclusión de nueva sección de valores públicos y ajustes en formato.",
                "observaciones": "Mejora en presentación de datos presupuestales."
            },
            {
                "version": "1.3",
                "fecha": f"2025-{self.mes:02d}-05",
                "responsable": "Coordinación Técnica",
                "descripcion": f"Actualización de datos del periodo {mes_nombre} {self.anio} y revisión de todas las secciones.",
                "observaciones": "Validación completa de datos y formato antes de entrega."
            },
            {
                "version": "1.4",
                "fecha": f"2025-{self.mes:02d}-{min(28, self.mes * 2)}",
                "responsable": "Coordinación Operativa",
                "descripcion": "Corrección de observaciones menores y actualización de anexos.",
                "observaciones": "Versión final para aprobación."
            }
        ]
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            df = pd.DataFrame(self.cambios)
            csv_demo = config.FUENTES_DIR / "control_cambios_demo.csv"
            df.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Cambios/Revisiones
            "cambios": self.cambios,
            "total_cambios": len(self.cambios),
            "hay_cambios": len(self.cambios) > 0,
        }

