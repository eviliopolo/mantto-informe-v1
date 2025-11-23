"""
Generador Sección 6: Visitas Técnicas / Inspecciones
Tipo: 🟩 EXTRACCIÓN DATOS (visitas, observaciones, hallazgos, seguimiento)

Subsecciones:
- 6.1 Visitas técnicas realizadas
- 6.2 Observaciones de las visitas
- 6.3 Hallazgos relevantes
- 6.4 Actividades de seguimiento
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
import config


class GeneradorSeccion6(GeneradorSeccion):
    """Genera la sección 6: Visitas Técnicas / Inspecciones"""
    
    @property
    def nombre_seccion(self) -> str:
        return "6. VISITAS TÉCNICAS / INSPECCIONES"
    
    @property
    def template_file(self) -> str:
        return "seccion_6_visitas.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.visitas: List[Dict] = []
        self.observaciones: List[Dict] = []
        self.hallazgos: List[Dict] = []
        self.seguimiento: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 6 desde JSON o genera datos dummy"""
        # Intentar cargar desde archivo JSON
        archivo = config.FUENTES_DIR / f"visitas_{self.mes}_{self.anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"visitas_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.visitas = data.get("visitas", [])
                    self.observaciones = data.get("observaciones", [])
                    self.hallazgos = data.get("hallazgos", [])
                    self.seguimiento = data.get("seguimiento", [])
            except Exception as e:
                print(f"[WARNING] Error al cargar datos desde {archivo}: {e}")
                self._generar_datos_dummy()
        else:
            # No hay fuente de datos, generar datos dummy
            print(f"[INFO] No se encontró archivo de datos, generando datos dummy para pruebas")
            self._generar_datos_dummy()
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        # 6.1 Visitas técnicas realizadas
        self.visitas = [
            {
                "lugar": "Subestación Norte",
                "fecha": f"2025-{self.mes:02d}-14",
                "responsable": "Técnico A",
                "descripcion": "Inspección general del estado de cámaras y switches."
            },
            {
                "lugar": "Localidad Kennedy - Sector Centro",
                "fecha": f"2025-{self.mes:02d}-18",
                "responsable": "Técnico B",
                "descripcion": "Verificación de infraestructura de red y equipos de comunicación."
            },
            {
                "lugar": "Subestación Sur",
                "fecha": f"2025-{self.mes:02d}-22",
                "responsable": "Técnico C",
                "descripcion": "Revisión de sistemas de alimentación y respaldo energético."
            }
        ]
        
        # 6.2 Observaciones de las visitas
        self.observaciones = [
            {
                "titulo": "Cableado expuesto",
                "detalle": "Se identificó tramo de cable UTP sin canalización en Subestación Norte."
            },
            {
                "titulo": "Equipos sin etiquetado",
                "detalle": "Falta de identificación en switches de Localidad Kennedy."
            },
            {
                "titulo": "Ventilación insuficiente",
                "detalle": "Sala técnica en Subestación Sur requiere mejor flujo de aire."
            }
        ]
        
        # 6.3 Hallazgos relevantes
        self.hallazgos = [
            {
                "hallazgo": "UPS sin autonomía suficiente",
                "impacto": "Alto",
                "fecha": f"2025-{self.mes:02d}-18"
            },
            {
                "hallazgo": "Conexión de red intermitente",
                "impacto": "Medio",
                "fecha": f"2025-{self.mes:02d}-20"
            },
            {
                "hallazgo": "Falta de respaldo de configuración",
                "impacto": "Medio",
                "fecha": f"2025-{self.mes:02d}-22"
            }
        ]
        
        # 6.4 Actividades de seguimiento
        self.seguimiento = [
            {
                "actividad": "Reposición de canalización",
                "estado": "En ejecución",
                "responsable": "Brigada de campo",
                "fecha": f"2025-{self.mes:02d}-20"
            },
            {
                "actividad": "Etiquetado de equipos",
                "estado": "Programado",
                "responsable": "Técnico de inventario",
                "fecha": f"2025-{self.mes:02d}-25"
            },
            {
                "actividad": "Actualización de UPS",
                "estado": "En evaluación",
                "responsable": "Coordinador técnico",
                "fecha": f"2025-{self.mes:02d}-28"
            }
        ]
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Narrativa fija
            "texto_intro": "Durante el presente periodo se realizaron visitas técnicas a diferentes puntos del sistema, con el fin de verificar el estado operativo, condiciones de infraestructura y cumplimiento de lineamientos.",
            
            # 6.1 Visitas técnicas realizadas
            "visitas": self.visitas,
            "total_visitas": len(self.visitas),
            "hay_visitas": len(self.visitas) > 0,
            
            # 6.2 Observaciones de las visitas
            "observaciones": self.observaciones,
            "total_observaciones": len(self.observaciones),
            "hay_observaciones": len(self.observaciones) > 0,
            
            # 6.3 Hallazgos relevantes
            "hallazgos": self.hallazgos,
            "total_hallazgos": len(self.hallazgos),
            "hay_hallazgos": len(self.hallazgos) > 0,
            
            # 6.4 Actividades de seguimiento
            "seguimiento": self.seguimiento,
            "total_seguimiento": len(self.seguimiento),
            "hay_seguimiento": len(self.seguimiento) > 0,
        }

