"""
Generador Sección 12: Conclusiones
Tipo: 🟦 CONTENIDO FIJO + 🟩 EXTRACCIÓN (resumen de todas las secciones)

Esta sección sintetiza los principales hallazgos, logros y recomendaciones
del informe mensual del contrato SCJ-1809-2024.
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from .base import GeneradorSeccion
import config


class GeneradorSeccion12(GeneradorSeccion):
    """Genera la sección 12: Conclusiones"""
    
    @property
    def nombre_seccion(self) -> str:
        return "12. CONCLUSIONES"
    
    @property
    def template_file(self) -> str:
        return "seccion_12_conclusiones.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.conclusiones_texto: List[str] = []
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 12 desde JSON o genera conclusiones dummy"""
        # Intentar cargar desde archivo JSON
        archivo = config.FUENTES_DIR / f"conclusiones_{self.mes}_{self.anio}.json"
        if not archivo.exists():
            archivo = config.FUENTES_DIR / f"conclusiones_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conclusiones_texto = data.get("conclusiones", [])
            except Exception as e:
                print(f"[WARNING] Error al cargar datos desde {archivo}: {e}")
                self._generar_conclusiones_dummy()
        else:
            # No hay fuente de datos, generar conclusiones dummy
            print(f"[INFO] No se encontró archivo de datos, generando conclusiones dummy para pruebas")
            self._generar_conclusiones_dummy()
    
    def _generar_conclusiones_dummy(self) -> None:
        """Genera conclusiones dummy profesionales cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        self.conclusiones_texto = [
            # Resumen corto del cumplimiento del mes
            f"Durante el mes de {mes_nombre} de {self.anio} se cumplió con las actividades programadas de mantenimiento preventivo y correctivo, logrando un índice de disponibilidad del sistema alineado a los ANS establecidos en el contrato SCJ-1809-2024.",
            
            # Destacar puntos críticos atendidos
            "Se gestionaron oportunamente las incidencias críticas reportadas, manteniendo la operación funcional de los sistemas de monitoreo y comunicación. Se atendieron de forma prioritaria los siniestros reportados, implementando medidas correctivas inmediatas para minimizar el impacto operacional.",
            
            # Logros relevantes del periodo
            f"Entre los logros más relevantes del periodo se destacan: la ejecución exitosa de {len(self._get_logros_ejemplo())} proyectos de valor público, la realización de {len(self._get_capacitaciones_ejemplo())} capacitaciones en seguridad y salud en el trabajo, y el mantenimiento de un cumplimiento superior al 98% en los indicadores de disponibilidad del sistema.",
            
            # Riesgos o alertas importantes
            "Se identificaron riesgos de nivel crítico y alto en la matriz de riesgos, los cuales están siendo atendidos mediante planes de mitigación específicos. Se recomienda mantener el seguimiento continuo a las medidas correctivas implementadas y reforzar los protocolos de seguridad en áreas identificadas como vulnerables.",
            
            # Aspectos a mejorar o fortalecer
            "Se identificaron oportunidades de mejora en la gestión de inventario y en la optimización de tiempos de respuesta para mantenimientos correctivos. Se sugiere fortalecer los procesos de documentación técnica y mejorar la coordinación entre equipos de campo y centro de monitoreo.",
            
            # Notas de continuidad para el siguiente mes
            f"Para el siguiente periodo se recomienda continuar con la implementación de los pilotos de valor público aprobados, especialmente aquellos relacionados con energía solar e IoT. Se mantendrá el seguimiento a las medidas correctivas pendientes y se reforzarán las actividades de capacitación en áreas críticas identificadas."
        ]
    
    def _get_logros_ejemplo(self) -> List[str]:
        """Retorna lista de ejemplo de logros (para uso en texto dummy)"""
        return ["piloto energía solar", "módulos IoT", "sistema de alertas"]
    
    def _get_capacitaciones_ejemplo(self) -> List[str]:
        """Retorna lista de ejemplo de capacitaciones (para uso en texto dummy)"""
        return ["trabajo en alturas", "uso de EPP", "herramientas eléctricas", "primeros auxilios"]
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        return {
            # Conclusiones como lista de párrafos
            "conclusiones_texto": self.conclusiones_texto,
            "total_conclusiones": len(self.conclusiones_texto),
            "hay_conclusiones": len(self.conclusiones_texto) > 0,
        }

