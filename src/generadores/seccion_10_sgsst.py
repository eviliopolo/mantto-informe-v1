"""
Generador Sección 10: Sistema de Gestión de Seguridad y Salud en el Trabajo - SG-SST
Tipo: 🟩 EXTRACCIÓN DATOS (capacitaciones, incidentes, EPP, inspecciones, COPASST)

Subsecciones:
- 10.1 Inducciones y capacitaciones
- 10.2 Reporte e investigación de incidentes / accidentes
- 10.3 Entrega de elementos de protección personal (EPP)
- 10.4 Inspecciones de seguridad
- 10.5 Actividades del COPASST
- 10.6 Medidas preventivas y correctivas
- 10.7 Seguimiento e indicadores del mes
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
from .base import GeneradorSeccion
import config


class GeneradorSeccion10(GeneradorSeccion):
    """Genera la sección 10: Sistema de Gestión de Seguridad y Salud en el Trabajo - SG-SST"""
    
    @property
    def nombre_seccion(self) -> str:
        return "10. SISTEMA DE GESTIÓN DE SEGURIDAD Y SALUD EN EL TRABAJO – SG-SST"
    
    @property
    def template_file(self) -> str:
        return "seccion_10_sgsst.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.capacitaciones: List[Dict] = []
        self.incidentes: List[Dict] = []
        self.epp: List[Dict] = []
        self.inspecciones: List[Dict] = []
        self.copasst: List[Dict] = []
        self.medidas_correctivas: List[Dict] = []
        self.indicadores: Dict[str, Any] = {}
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 10 desde CSV o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "sgsst.csv"
        
        datos_cargados = False
        
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
                # Procesar datos según estructura del CSV
                # Asumir que el CSV tiene columnas que permiten separar por tipo
                self._procesar_datos_csv(df)
                datos_cargados = True
                print(f"[INFO] Datos cargados desde CSV: {archivo_csv}")
            except Exception as e:
                print(f"[WARNING] Error al cargar CSV {archivo_csv}: {e}")
        
        # Si no hay datos, generar dummy
        if not datos_cargados:
            print(f"[INFO] No se encontraron fuentes de datos, generando datos dummy para pruebas")
            self._generar_datos_dummy()
            self._guardar_csv_demo()
    
    def _procesar_datos_csv(self, df: pd.DataFrame) -> None:
        """Procesa datos desde CSV y los convierte al formato esperado"""
        # Adaptar según estructura real del CSV
        # Por ahora, asumir estructura simple
        if 'tipo' in df.columns:
            # Separar por tipo de registro
            if 'capacitacion' in df['tipo'].values:
                self.capacitaciones = df[df['tipo'] == 'capacitacion'].to_dict('records')
            if 'incidente' in df['tipo'].values:
                self.incidentes = df[df['tipo'] == 'incidente'].to_dict('records')
            # ... etc
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        # 10.1 Inducciones y capacitaciones
        self.capacitaciones = [
            {
                "tema": "Trabajo seguro en alturas",
                "fecha": f"2025-{self.mes:02d}-03",
                "participantes": 12,
                "responsable": "HSE"
            },
            {
                "tema": "Uso adecuado de EPP",
                "fecha": f"2025-{self.mes:02d}-10",
                "participantes": 18,
                "responsable": "Seguridad Industrial"
            },
            {
                "tema": "Manejo de herramientas eléctricas",
                "fecha": f"2025-{self.mes:02d}-15",
                "participantes": 15,
                "responsable": "HSE"
            },
            {
                "tema": "Primeros auxilios básicos",
                "fecha": f"2025-{self.mes:02d}-20",
                "participantes": 20,
                "responsable": "Brigada de Emergencias"
            }
        ]
        
        # 10.2 Reporte e investigación de incidentes / accidentes
        self.incidentes = [
            {
                "fecha": f"2025-{self.mes:02d}-11",
                "tipo": "Incidente sin lesión",
                "descripcion": "Resbalón en área húmeda sin consecuencias",
                "clasificacion": "Leve",
                "accion_tomada": "Secado de área, señalización preventiva y capacitación"
            },
            {
                "fecha": f"2025-{self.mes:02d}-18",
                "tipo": "Cuasi accidente",
                "descripcion": "Caída de herramienta desde altura sin impacto",
                "clasificacion": "Leve",
                "accion_tomada": "Refuerzo de protocolos de trabajo en alturas"
            }
        ]
        
        # 10.3 Entrega de elementos de protección personal (EPP)
        self.epp = [
            {
                "item": "Casco dieléctrico",
                "cantidad": 5,
                "fecha": f"2025-{self.mes:02d}-05",
                "entregado_a": "Equipo Técnico"
            },
            {
                "item": "Guantes anticorte",
                "cantidad": 12,
                "fecha": f"2025-{self.mes:02d}-07",
                "entregado_a": "Personal de campo"
            },
            {
                "item": "Gafas de seguridad",
                "cantidad": 8,
                "fecha": f"2025-{self.mes:02d}-12",
                "entregado_a": "Brigada de mantenimiento"
            },
            {
                "item": "Botas de seguridad dieléctricas",
                "cantidad": 10,
                "fecha": f"2025-{self.mes:02d}-18",
                "entregado_a": "Equipo de instalación"
            }
        ]
        
        # 10.4 Inspecciones de seguridad
        self.inspecciones = [
            {
                "lugar": "Bodega Central",
                "fecha": f"2025-{self.mes:02d}-08",
                "estado": "Cumple",
                "observaciones": "Sin novedades, condiciones seguras"
            },
            {
                "lugar": "Centro de Monitoreo",
                "fecha": f"2025-{self.mes:02d}-12",
                "estado": "No cumple",
                "observaciones": "Extintor sin recarga, requiere acción inmediata"
            },
            {
                "lugar": "Taller de Reparaciones",
                "fecha": f"2025-{self.mes:02d}-16",
                "estado": "Cumple con observaciones",
                "observaciones": "Mejorar orden y limpieza en área de herramientas"
            },
            {
                "lugar": "Oficinas Administrativas",
                "fecha": f"2025-{self.mes:02d}-22",
                "estado": "Cumple",
                "observaciones": "Sin novedades"
            }
        ]
        
        # 10.5 Actividades del COPASST
        self.copasst = [
            {
                "actividad": "Reunión mensual COPASST",
                "fecha": f"2025-{self.mes:02d}-04",
                "acuerdos": "Actualizar matriz de peligros y revisar protocolos de emergencia"
            },
            {
                "actividad": "Revisión de indicadores de seguridad",
                "fecha": f"2025-{self.mes:02d}-14",
                "acuerdos": "Implementar acciones correctivas para áreas identificadas"
            },
            {
                "actividad": "Capacitación a miembros COPASST",
                "fecha": f"2025-{self.mes:02d}-25",
                "acuerdos": "Actualización en normativa de seguridad y salud en el trabajo"
            }
        ]
        
        # 10.6 Medidas preventivas y correctivas
        self.medidas_correctivas = [
            {
                "medida": "Recarga de extintores",
                "responsable": "Infraestructura",
                "fecha_compromiso": f"2025-{self.mes:02d}-20",
                "estado": "En ejecución"
            },
            {
                "medida": "Mejora de señalización en áreas húmedas",
                "responsable": "HSE",
                "fecha_compromiso": f"2025-{self.mes:02d}-15",
                "estado": "Completado"
            },
            {
                "medida": "Reorganización de área de herramientas",
                "responsable": "Brigada de Mantenimiento",
                "fecha_compromiso": f"2025-{self.mes:02d}-28",
                "estado": "Programado"
            }
        ]
        
        # 10.7 Seguimiento e indicadores del mes
        total_personal = 45  # Ejemplo
        total_capacitados = sum(cap.get("participantes", 0) for cap in self.capacitaciones)
        porcentaje_capacitacion = round((total_capacitados / total_personal) * 100, 2) if total_personal > 0 else 0
        
        inspecciones_cumplen = sum(1 for ins in self.inspecciones if ins.get("estado") == "Cumple")
        porcentaje_cumplimiento = round((inspecciones_cumplen / len(self.inspecciones)) * 100, 2) if self.inspecciones else 0
        
        self.indicadores = {
            "accidentalidad": "0 casos con lesión",
            "porcentaje_capacitacion": porcentaje_capacitacion,
            "cumplimiento_inspecciones": porcentaje_cumplimiento,
            "total_capacitaciones": len(self.capacitaciones),
            "total_incidentes": len(self.incidentes),
            "total_epp_entregado": sum(e.get("cantidad", 0) for e in self.epp),
            "total_inspecciones": len(self.inspecciones),
            "total_medidas": len(self.medidas_correctivas)
        }
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            # Crear DataFrame combinado para demo
            datos_demo = []
            
            # Agregar capacitaciones
            for cap in self.capacitaciones:
                datos_demo.append({
                    "tipo": "capacitacion",
                    "tema": cap.get("tema", ""),
                    "fecha": cap.get("fecha", ""),
                    "participantes": cap.get("participantes", 0),
                    "responsable": cap.get("responsable", "")
                })
            
            # Agregar incidentes
            for inc in self.incidentes:
                datos_demo.append({
                    "tipo": "incidente",
                    "fecha": inc.get("fecha", ""),
                    "tipo_incidente": inc.get("tipo", ""),
                    "descripcion": inc.get("descripcion", ""),
                    "clasificacion": inc.get("clasificacion", ""),
                    "accion_tomada": inc.get("accion_tomada", "")
                })
            
            # Agregar EPP
            for e in self.epp:
                datos_demo.append({
                    "tipo": "epp",
                    "item": e.get("item", ""),
                    "cantidad": e.get("cantidad", 0),
                    "fecha": e.get("fecha", ""),
                    "entregado_a": e.get("entregado_a", "")
                })
            
            df = pd.DataFrame(datos_demo)
            csv_demo = config.FUENTES_DIR / "sgsst_dummy.csv"
            df.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Narrativa fija
            "texto_intro": "Durante el periodo evaluado se desarrollaron las actividades asociadas al Sistema de Gestión de Seguridad y Salud en el Trabajo, incluyendo capacitaciones, inspecciones, seguimiento a EPP y control de incidentes, alineadas con los lineamientos del contrato SCJ-1809-2024.",
            
            # 10.1 Inducciones y capacitaciones
            "capacitaciones": self.capacitaciones,
            "total_capacitaciones": len(self.capacitaciones),
            "hay_capacitaciones": len(self.capacitaciones) > 0,
            
            # 10.2 Reporte e investigación de incidentes
            "incidentes": self.incidentes,
            "total_incidentes": len(self.incidentes),
            "hay_incidentes": len(self.incidentes) > 0,
            
            # 10.3 Entrega de EPP
            "epp": self.epp,
            "total_epp": len(self.epp),
            "hay_epp": len(self.epp) > 0,
            
            # 10.4 Inspecciones de seguridad
            "inspecciones": self.inspecciones,
            "total_inspecciones": len(self.inspecciones),
            "hay_inspecciones": len(self.inspecciones) > 0,
            
            # 10.5 Actividades del COPASST
            "copasst": self.copasst,
            "total_copasst": len(self.copasst),
            "hay_copasst": len(self.copasst) > 0,
            
            # 10.6 Medidas preventivas y correctivas
            "medidas_correctivas": self.medidas_correctivas,
            "total_medidas": len(self.medidas_correctivas),
            "hay_medidas": len(self.medidas_correctivas) > 0,
            
            # 10.7 Indicadores
            "indicadores": self.indicadores,
        }

