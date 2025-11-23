"""
Generador Sección 11: Valores Públicos
Tipo: 🟩 EXTRACCIÓN DATOS (pilotos, proyectos, actas, evidencias, indicadores)

Subsecciones:
- 11.1 Pilotos e iniciativas de valor público
- 11.2 Proyectos aprobados y en implementación
- 11.3 Aprobaciones / actas y soportes
- 11.4 Resultados cuantitativos y evidencias
- 11.5 Recomendaciones y próximos pasos
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
from .base import GeneradorSeccion
from src.utils.formato_moneda import formato_moneda_cop
import config


class GeneradorSeccion11(GeneradorSeccion):
    """Genera la sección 11: Valores Públicos"""
    
    @property
    def nombre_seccion(self) -> str:
        return "11. VALORES PÚBLICOS"
    
    @property
    def template_file(self) -> str:
        return "seccion_11_valores.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.pilotos: List[Dict] = []
        self.proyectos: List[Dict] = []
        self.actas_soportes: List[Dict] = []
        self.evidencias: List[Dict] = []
        self.indicadores: Dict[str, Any] = {}
        self.recomendaciones: str = ""
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 11 desde CSV o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "valores_publicos.csv"
        
        datos_cargados = False
        
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
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
        if 'tipo' in df.columns:
            if 'piloto' in df['tipo'].values:
                self.pilotos = df[df['tipo'] == 'piloto'].to_dict('records')
            if 'proyecto' in df['tipo'].values:
                self.proyectos = df[df['tipo'] == 'proyecto'].to_dict('records')
            # ... etc
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        # 11.1 Pilotos e iniciativas de valor público
        self.pilotos = [
            {
                "titulo": "Piloto puntos con energía solar",
                "descripcion": "Implementación de paneles solares en 5 puntos piloto para continuidad de cámaras en caso de fallas eléctricas",
                "estado": "Aprobado",
                "fecha_aprobacion": f"2025-{self.mes-1:02d}-20" if self.mes > 1 else f"2024-12-20",
                "responsable": "Innovación ETB",
                "valor_aprobado": 32000000,
                "valor_aprobado_formato": formato_moneda_cop(32000000)
            },
            {
                "titulo": "Módulos de mantenimiento IoT",
                "descripcion": "Piloto de módulos IoT para reporte automático de estado de equipos y mantenimiento predictivo",
                "estado": "En implementación",
                "fecha_aprobacion": f"2025-{self.mes:02d}-02",
                "responsable": "I+D",
                "valor_aprobado": 18000000,
                "valor_aprobado_formato": formato_moneda_cop(18000000)
            },
            {
                "titulo": "Sistema de alertas tempranas",
                "descripcion": "Piloto de sistema de alertas tempranas basado en análisis de video para detección de situaciones de riesgo",
                "estado": "En evaluación",
                "fecha_aprobacion": f"2025-{self.mes:02d}-10",
                "responsable": "Innovación ETB",
                "valor_aprobado": 25000000,
                "valor_aprobado_formato": formato_moneda_cop(25000000)
            }
        ]
        
        # 11.2 Proyectos aprobados y en implementación
        self.proyectos = [
            {
                "nombre": "Integración estación piloto colegio",
                "alcance": "Integración de cámaras y conectividad en 1 colegio piloto para validación de modelo",
                "estado": "Culminado",
                "fecha_inicio": f"2025-{self.mes-2:02d}-10" if self.mes > 2 else f"2024-{12+self.mes-2:02d}-10",
                "fecha_fin": f"2025-{self.mes-1:02d}-30" if self.mes > 1 else f"2024-12-30",
                "coste": 9500000,
                "coste_formato": formato_moneda_cop(9500000)
            },
            {
                "nombre": "Ampliación cobertura Kennedy",
                "alcance": "Instalación de 15 nuevas cámaras en sector crítico de Kennedy",
                "estado": "En ejecución",
                "fecha_inicio": f"2025-{self.mes:02d}-05",
                "fecha_fin": f"2025-{self.mes+1:02d}-15" if self.mes < 12 else f"2026-01-15",
                "coste": 45000000,
                "coste_formato": formato_moneda_cop(45000000)
            },
            {
                "nombre": "Mejora infraestructura red",
                "alcance": "Actualización de switches y routers en 3 subestaciones principales",
                "estado": "Programado",
                "fecha_inicio": f"2025-{self.mes+1:02d}-01" if self.mes < 12 else f"2026-01-01",
                "fecha_fin": f"2025-{self.mes+2:02d}-20" if self.mes < 11 else f"2026-02-20",
                "coste": 68000000,
                "coste_formato": formato_moneda_cop(68000000)
            }
        ]
        
        # 11.3 Aprobaciones / actas y soportes
        self.actas_soportes = [
            {
                "tipo": "Acta aprobación PVV",
                "numero": "PVV-001-2025",
                "fecha": f"2025-{self.mes-1:02d}-21" if self.mes > 1 else f"2024-12-21",
                "url_soporte": "{{ soporte_pvv_001 }}"
            },
            {
                "tipo": "Acta aprobación PVV",
                "numero": "PVV-002-2025",
                "fecha": f"2025-{self.mes:02d}-05",
                "url_soporte": "{{ soporte_pvv_002 }}"
            },
            {
                "tipo": "Acta comité técnico",
                "numero": "CT-045-2025",
                "fecha": f"2025-{self.mes:02d}-12",
                "url_soporte": "{{ soporte_ct_045 }}"
            }
        ]
        
        # 11.4 Resultados cuantitativos y evidencias
        self.evidencias = [
            {
                "tipo": "Foto",
                "descripcion": "Instalación panel solar punto A",
                "ruta": "{{ evidencia_1_img }}"
            },
            {
                "tipo": "Documento",
                "descripcion": "Reporte técnico piloto IoT",
                "ruta": "{{ evidencia_2_pdf }}"
            },
            {
                "tipo": "Foto",
                "descripcion": "Integración cámaras colegio piloto",
                "ruta": "{{ evidencia_3_img }}"
            },
            {
                "tipo": "Video",
                "descripcion": "Demostración sistema alertas tempranas",
                "ruta": "{{ evidencia_4_video }}"
            }
        ]
        
        # Indicadores
        self.indicadores = {
            "puntos_solar_operativos": 5,
            "reduccion_fallos_energia_pct": 30,
            "pvvs_aprobados": 2,
            "proyectos_culminados": 1,
            "proyectos_en_ejecucion": 1,
            "proyectos_programados": 1,
            "total_inversion_aprobada": sum(p.get("valor_aprobado", 0) for p in self.pilotos),
            "total_inversion_aprobada_formato": formato_moneda_cop(sum(p.get("valor_aprobado", 0) for p in self.pilotos))
        }
        
        # 11.5 Recomendaciones y próximos pasos
        self.recomendaciones = """Se recomienda continuar con la implementación de los pilotos aprobados, especialmente el de energía solar que ha mostrado resultados positivos. Se sugiere escalar el piloto IoT a más puntos una vez validada su efectividad. Para los próximos meses se propone evaluar la incorporación de tecnologías de inteligencia artificial para análisis predictivo de mantenimiento."""
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            # Crear DataFrame combinado para demo
            datos_demo = []
            
            # Agregar pilotos
            for p in self.pilotos:
                datos_demo.append({
                    "tipo": "piloto",
                    "titulo": p.get("titulo", ""),
                    "descripcion": p.get("descripcion", ""),
                    "estado": p.get("estado", ""),
                    "fecha_aprobacion": p.get("fecha_aprobacion", ""),
                    "responsable": p.get("responsable", ""),
                    "valor_aprobado": p.get("valor_aprobado", 0)
                })
            
            # Agregar proyectos
            for pr in self.proyectos:
                datos_demo.append({
                    "tipo": "proyecto",
                    "nombre": pr.get("nombre", ""),
                    "alcance": pr.get("alcance", ""),
                    "estado": pr.get("estado", ""),
                    "fecha_inicio": pr.get("fecha_inicio", ""),
                    "fecha_fin": pr.get("fecha_fin", ""),
                    "coste": pr.get("coste", 0)
                })
            
            df = pd.DataFrame(datos_demo)
            csv_demo = config.FUENTES_DIR / "valores_publicos_demo.csv"
            df.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Narrativa fija
            "texto_intro": "En el periodo se avanzó en proyectos de valor público orientados a aumentar la resiliencia operacional y la incorporación de tecnologías IoT para mantenimiento predictivo. A continuación se resumen pilotos, aprobaciones y evidencias.",
            
            # 11.1 Pilotos e iniciativas
            "pilotos": self.pilotos,
            "total_pilotos": len(self.pilotos),
            "hay_pilotos": len(self.pilotos) > 0,
            
            # 11.2 Proyectos aprobados
            "proyectos": self.proyectos,
            "total_proyectos": len(self.proyectos),
            "hay_proyectos": len(self.proyectos) > 0,
            
            # 11.3 Actas y soportes
            "actas_soportes": self.actas_soportes,
            "total_actas": len(self.actas_soportes),
            "hay_actas": len(self.actas_soportes) > 0,
            
            # 11.4 Resultados cuantitativos y evidencias
            "evidencias": self.evidencias,
            "total_evidencias": len(self.evidencias),
            "hay_evidencias": len(self.evidencias) > 0,
            "indicadores": self.indicadores,
            
            # 11.5 Recomendaciones
            "recomendaciones": self.recomendaciones,
        }

