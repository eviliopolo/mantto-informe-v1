"""
Generador Sección 7: Registro de Siniestros / Eventos / Incidentes
Tipo: 🟩 EXTRACCIÓN DATOS (siniestros, afectaciones, acciones, seguimiento)

Subsecciones:
- 7.1 Siniestros reportados
- 7.2 Afectaciones a infraestructura
- 7.3 Acciones tomadas
- 7.4 Seguimiento a casos
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
import config


class GeneradorSeccion7(GeneradorSeccion):
    """Genera la sección 7: Registro de Siniestros / Eventos / Incidentes"""
    
    @property
    def nombre_seccion(self) -> str:
        return "7. REGISTRO DE SINIESTROS / EVENTOS / INCIDENTES"
    
    @property
    def template_file(self) -> str:
        return "seccion_7_siniestros.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.siniestros: List[Dict] = []
        self.afectaciones: List[Dict] = []
        self.acciones: List[Dict] = []
        self.seguimiento: List[Dict] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 7 desde JSON o genera datos dummy"""
        # Intentar cargar desde archivo JSON
        archivo = config.FUENTES_DIR / f"siniestros_{self.mes}_{self.anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"siniestros_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.siniestros = data.get("siniestros", [])
                    self.afectaciones = data.get("afectaciones", [])
                    self.acciones = data.get("acciones", [])
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
        
        # 7.1 Siniestros reportados
        self.siniestros = [
            {
                "fecha": f"2025-{self.mes:02d}-10",
                "lugar": "Estación de Policía Engativá",
                "tipo": "Vandalismo",
                "descripcion": "Cámara tipo domo impactada por objeto contundente."
            },
            {
                "fecha": f"2025-{self.mes:02d}-15",
                "lugar": "Subestación Norte",
                "tipo": "Falla eléctrica",
                "descripcion": "Corte de energía prolongado afectó sistema de respaldo."
            },
            {
                "fecha": f"2025-{self.mes:02d}-20",
                "lugar": "Localidad Kennedy",
                "tipo": "Robo",
                "descripcion": "Sustracción de cableado de red y equipos de conexión."
            }
        ]
        
        # 7.2 Afectaciones a infraestructura
        self.afectaciones = [
            {
                "componente": "Cámara Domo",
                "daño": "Cúpula fracturada",
                "impacto": "Pérdida de grabación",
                "fecha": f"2025-{self.mes:02d}-10"
            },
            {
                "componente": "UPS",
                "daño": "Baterías descargadas",
                "impacto": "Sistema sin respaldo energético",
                "fecha": f"2025-{self.mes:02d}-15"
            },
            {
                "componente": "Switch POE",
                "daño": "Equipo sustraído",
                "impacto": "Pérdida de conectividad en sector",
                "fecha": f"2025-{self.mes:02d}-20"
            }
        ]
        
        # 7.3 Acciones tomadas
        self.acciones = [
            {
                "accion": "Desmonte del equipo",
                "responsable": "Técnico Operaciones",
                "fecha": f"2025-{self.mes:02d}-11",
                "estado": "Ejecutado"
            },
            {
                "accion": "Reemplazo de baterías UPS",
                "responsable": "Brigada de mantenimiento",
                "fecha": f"2025-{self.mes:02d}-16",
                "estado": "Ejecutado"
            },
            {
                "accion": "Denuncia ante autoridades",
                "responsable": "Coordinación Técnica",
                "fecha": f"2025-{self.mes:02d}-21",
                "estado": "En trámite"
            },
            {
                "accion": "Instalación de equipo de reemplazo",
                "responsable": "Técnico de campo",
                "fecha": f"2025-{self.mes:02d}-25",
                "estado": "Programado"
            }
        ]
        
        # 7.4 Seguimiento a casos
        self.seguimiento = [
            {
                "actividad": "Gestión de reposición de domo",
                "estado": "En trámite",
                "fecha_compromiso": f"2025-{self.mes:02d}-20",
                "responsable": "Coordinación Técnica"
            },
            {
                "actividad": "Verificación de sistema de respaldo",
                "estado": "Completado",
                "fecha_compromiso": f"2025-{self.mes:02d}-18",
                "responsable": "Ingeniero de soporte"
            },
            {
                "actividad": "Reposición de switch sustraído",
                "estado": "En evaluación",
                "fecha_compromiso": f"2025-{self.mes:02d}-28",
                "responsable": "Coordinación Técnica"
            }
        ]
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Narrativa fija
            "texto_intro": "Durante el presente periodo se registraron diferentes siniestros y eventos que afectaron la operación de los sistemas asociados al contrato SCJ-1809-2024. A continuación, se describen los casos identificados, las acciones tomadas y el seguimiento correspondiente.",
            
            # 7.1 Siniestros reportados
            "siniestros": self.siniestros,
            "total_siniestros": len(self.siniestros),
            "hay_siniestros": len(self.siniestros) > 0,
            
            # 7.2 Afectaciones a infraestructura
            "afectaciones": self.afectaciones,
            "total_afectaciones": len(self.afectaciones),
            "hay_afectaciones": len(self.afectaciones) > 0,
            
            # 7.3 Acciones tomadas
            "acciones": self.acciones,
            "total_acciones": len(self.acciones),
            "hay_acciones": len(self.acciones) > 0,
            
            # 7.4 Seguimiento a casos
            "seguimiento": self.seguimiento,
            "total_seguimiento": len(self.seguimiento),
            "hay_seguimiento": len(self.seguimiento) > 0,
        }

