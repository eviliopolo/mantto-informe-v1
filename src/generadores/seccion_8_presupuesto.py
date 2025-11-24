"""
Generador Sección 8: Ejecución Presupuestal
Tipo: 🟩 EXTRACCIÓN DATOS (presupuesto, ejecución, compras, variaciones)

Subsecciones:
- 8.1 Ejecución mensual
- 8.2 Consolidado presupuestal contrato
- 8.3 Compras y uso de la bolsa de repuestos
- 8.4 Variaciones presupuestales y justificaciones
- 8.5 Observaciones y recomendaciones
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
from .base import GeneradorSeccion
from src.utils.formato_moneda import formato_moneda_cop
import config


class GeneradorSeccion8(GeneradorSeccion):
    """Genera la sección 8: Ejecución Presupuestal"""
    
    @property
    def nombre_seccion(self) -> str:
        return "8. EJECUCIÓN PRESUPUESTAL"
    
    @property
    def template_file(self) -> str:
        return "seccion_8_presupuesto.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.ejecucion_mensual: List[Dict] = []
        self.consolidado: List[Dict] = []
        self.compras_bolsa: List[Dict] = []
        self.variaciones: List[Dict] = []
        self.grafico_ejecucion_img: str = ""
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 8 desde CSV/JSON o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "ejecucion_presupuestal.csv"
        archivo_json = config.FUENTES_DIR / f"ejecucion_presupuestal_{self.mes}_{self.anio}.json"
        
        if not archivo_json.exists():
            archivo_json = config.FUENTES_DIR / f"ejecucion_presupuestal_{config.MESES[self.mes].lower()}_{self.anio}.json"
        
        datos_cargados = False
        
        # Intentar cargar desde CSV
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
                self._procesar_datos_csv(df)
                datos_cargados = True
                print(f"[INFO] Datos cargados desde CSV: {archivo_csv}")
            except Exception as e:
                print(f"[WARNING] Error al cargar CSV {archivo_csv}: {e}")
        
        # Intentar cargar desde JSON
        if not datos_cargados and archivo_json.exists():
            try:
                with open(archivo_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ejecucion_mensual = data.get("ejecucion_mensual", [])
                    self.consolidado = data.get("consolidado", [])
                    self.compras_bolsa = data.get("compras_bolsa", [])
                    self.variaciones = data.get("variaciones", [])
                
                # Calcular porcentajes y formatear valores para ejecución mensual
                self._procesar_ejecucion_mensual()
                
                # Calcular porcentajes y formatear valores para consolidado
                self._procesar_consolidado()
                
                # Formatear valores para compras bolsa
                self._procesar_compras_bolsa()
                
                datos_cargados = True
                print(f"[INFO] Datos cargados desde JSON: {archivo_json}")
            except Exception as e:
                print(f"[WARNING] Error al cargar JSON {archivo_json}: {e}")
        
        # Si no hay datos, generar dummy
        if not datos_cargados:
            print(f"[INFO] No se encontraron fuentes de datos, generando datos dummy para pruebas")
            self._generar_datos_dummy()
            self._guardar_csv_demo()
    
    def _procesar_datos_csv(self, df: pd.DataFrame) -> None:
        """Procesa datos desde CSV y los convierte al formato esperado"""
        # Asumir estructura CSV con columnas: categoria, presupuesto, ejecutado, mes, etc.
        # Adaptar según estructura real del CSV
        if 'categoria' in df.columns:
            self.ejecucion_mensual = df[['categoria', 'presupuesto', 'ejecutado']].to_dict('records')
            # Calcular porcentajes y formatear valores
            self._procesar_ejecucion_mensual()
        
        if 'mes' in df.columns:
            self.consolidado = df[['mes', 'presupuesto_mes', 'ejecutado_mes']].to_dict('records')
            # Calcular porcentajes y formatear valores
            self._procesar_consolidado()
    
    def _procesar_ejecucion_mensual(self) -> None:
        """Calcula porcentajes y formatea valores para ejecución mensual"""
        for item in self.ejecucion_mensual:
            presupuesto = item.get("presupuesto", 0)
            ejecutado = item.get("ejecutado", 0)
            if presupuesto > 0:
                item["porcentaje_ejecucion"] = round((ejecutado / presupuesto) * 100, 2)
            else:
                item["porcentaje_ejecucion"] = 0.0
            # Formatear valores monetarios
            item["presupuesto_formato"] = formato_moneda_cop(presupuesto)
            item["ejecutado_formato"] = formato_moneda_cop(ejecutado)
    
    def _procesar_consolidado(self) -> None:
        """Calcula porcentajes y formatea valores para consolidado"""
        for item in self.consolidado:
            presupuesto = item.get("presupuesto_mes", 0)
            ejecutado = item.get("ejecutado_mes", 0)
            if presupuesto > 0:
                item["porcentaje_ejecucion"] = round((ejecutado / presupuesto) * 100, 2)
            else:
                item["porcentaje_ejecucion"] = 0.0
            # Formatear valores monetarios
            item["presupuesto_mes_formato"] = formato_moneda_cop(presupuesto)
            item["ejecutado_mes_formato"] = formato_moneda_cop(ejecutado)
    
    def _procesar_compras_bolsa(self) -> None:
        """Formatea valores monetarios para compras bolsa"""
        for item in self.compras_bolsa:
            item["valor_unitario_formato"] = formato_moneda_cop(item.get("valor_unitario", 0))
            item["valor_total_formato"] = formato_moneda_cop(item.get("valor_total", 0))
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        # 8.1 Ejecución mensual
        self.ejecucion_mensual = [
            {
                "categoria": "Mano de obra",
                "presupuesto": 200000000,
                "ejecutado": 180000000
            },
            {
                "categoria": "Repuestos",
                "presupuesto": 50000000,
                "ejecutado": 42000000
            },
            {
                "categoria": "Gastos operativos",
                "presupuesto": 30000000,
                "ejecutado": 25000000
            },
            {
                "categoria": "Servicios técnicos",
                "presupuesto": 40000000,
                "ejecutado": 38000000
            }
        ]
        
        # Calcular porcentajes de ejecución y formatear valores
        for item in self.ejecucion_mensual:
            presupuesto = item.get("presupuesto", 0)
            ejecutado = item.get("ejecutado", 0)
            if presupuesto > 0:
                item["porcentaje_ejecucion"] = round((ejecutado / presupuesto) * 100, 2)
            else:
                item["porcentaje_ejecucion"] = 0.0
            # Formatear valores monetarios para el template
            item["presupuesto_formato"] = formato_moneda_cop(presupuesto)
            item["ejecutado_formato"] = formato_moneda_cop(ejecutado)
        
        # 8.2 Consolidado presupuestal
        self.consolidado = [
            {
                "mes": "Julio 2025",
                "presupuesto_mes": 280000000,
                "ejecutado_mes": 247000000
            },
            {
                "mes": "Agosto 2025",
                "presupuesto_mes": 280000000,
                "ejecutado_mes": 260000000
            },
            {
                "mes": f"{mes_nombre} {self.anio}",
                "presupuesto_mes": 280000000,
                "ejecutado_mes": 270000000
            }
        ]
        
        # Calcular porcentajes de ejecución para consolidado y formatear valores
        for item in self.consolidado:
            presupuesto = item.get("presupuesto_mes", 0)
            ejecutado = item.get("ejecutado_mes", 0)
            if presupuesto > 0:
                item["porcentaje_ejecucion"] = round((ejecutado / presupuesto) * 100, 2)
            else:
                item["porcentaje_ejecucion"] = 0.0
            # Formatear valores monetarios para el template
            item["presupuesto_mes_formato"] = formato_moneda_cop(presupuesto)
            item["ejecutado_mes_formato"] = formato_moneda_cop(ejecutado)
        
        # 8.3 Compras y uso de la bolsa de repuestos
        self.compras_bolsa = [
            {
                "item": "Cámara Domo",
                "cantidad": 10,
                "valor_unitario": 1200000,
                "valor_total": 12000000,
                "fecha": f"2025-{self.mes:02d}-05"
            },
            {
                "item": "Fuente PoE",
                "cantidad": 5,
                "valor_unitario": 450000,
                "valor_total": 2250000,
                "fecha": f"2025-{self.mes:02d}-12"
            },
            {
                "item": "Switch POE 8 puertos",
                "cantidad": 3,
                "valor_unitario": 850000,
                "valor_total": 2550000,
                "fecha": f"2025-{self.mes:02d}-18"
            },
            {
                "item": "Batería 12V 7AH",
                "cantidad": 20,
                "valor_unitario": 165000,
                "valor_total": 3300000,
                "fecha": f"2025-{self.mes:02d}-22"
            }
        ]
        
        # Formatear valores monetarios para compras bolsa
        for item in self.compras_bolsa:
            item["valor_unitario_formato"] = formato_moneda_cop(item.get("valor_unitario", 0))
            item["valor_total_formato"] = formato_moneda_cop(item.get("valor_total", 0))
        
        # 8.4 Variaciones presupuestales
        self.variaciones = [
            {
                "categoria": "Repuestos",
                "variacion": -16.0,
                "explicacion": "Ajuste por compras centralizadas y descuentos por volumen"
            },
            {
                "categoria": "Mano de obra",
                "variacion": -10.0,
                "explicacion": "Optimización de jornadas y reasignación de tareas"
            },
            {
                "categoria": "Gastos operativos",
                "variacion": -16.67,
                "explicacion": "Reducción en costos de desplazamiento y optimización de rutas"
            }
        ]
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            # Crear DataFrame con ejecución mensual
            df_ejecucion = pd.DataFrame(self.ejecucion_mensual)
            
            # Guardar CSV de ejemplo
            csv_demo = config.FUENTES_DIR / "ejecucion_presupuestal_demo.csv"
            df_ejecucion.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def _calcular_totales(self) -> Dict[str, Any]:
        """Calcula totales y resúmenes presupuestales"""
        total_presupuesto = sum(item.get("presupuesto", 0) for item in self.ejecucion_mensual)
        total_ejecutado = sum(item.get("ejecutado", 0) for item in self.ejecucion_mensual)
        
        porcentaje_total = 0.0
        if total_presupuesto > 0:
            porcentaje_total = round((total_ejecutado / total_presupuesto) * 100, 2)
        
        total_compras_bolsa = sum(item.get("valor_total", 0) for item in self.compras_bolsa)
        
        return {
            "total_presupuesto": total_presupuesto,
            "total_ejecutado": total_ejecutado,
            "porcentaje_total_ejecucion": porcentaje_total,
            "total_compras_bolsa": total_compras_bolsa
        }
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        # Calcular totales
        totales = self._calcular_totales()
        
        return {
            # Narrativa fija
            "texto_intro": f"Durante el periodo de {config.MESES[self.mes]} de {self.anio} se presenta el reporte de ejecución presupuestal del contrato SCJ-1809-2024, detallando el uso de recursos asignados y las variaciones identificadas.",
            
            # 8.1 Ejecución mensual
            "ejecucion_mensual": self.ejecucion_mensual,
            "total_ejecucion_mensual": len(self.ejecucion_mensual),
            "hay_ejecucion_mensual": len(self.ejecucion_mensual) > 0,
            
            # 8.2 Consolidado presupuestal
            "consolidado": self.consolidado,
            "total_consolidado": len(self.consolidado),
            "hay_consolidado": len(self.consolidado) > 0,
            
            # 8.3 Compras y uso de la bolsa
            "compras_bolsa": self.compras_bolsa,
            "total_compras_bolsa": len(self.compras_bolsa),
            "hay_compras_bolsa": len(self.compras_bolsa) > 0,
            
            # 8.4 Variaciones presupuestales
            "variaciones": self.variaciones,
            "total_variaciones": len(self.variaciones),
            "hay_variaciones": len(self.variaciones) > 0,
            
            # Totales calculados
            **totales,
            
            # Formatear totales para el template
            "total_presupuesto_formato": formato_moneda_cop(totales["total_presupuesto"]),
            "total_ejecutado_formato": formato_moneda_cop(totales["total_ejecutado"]),
            "total_compras_bolsa_formato": formato_moneda_cop(totales["total_compras_bolsa"]),
            
            # Variables adicionales
            "periodo": f"{config.MESES[self.mes]} {self.anio}",
            "contrato_numero": "SCJ-1809-2024",
            
            # Placeholder para gráfico (si se genera)
            "grafico_ejecucion_img": self.grafico_ejecucion_img,
            
            # 8.5 Observaciones y recomendaciones (texto fijo por ahora)
            "observaciones": "La ejecución presupuestal del periodo muestra un cumplimiento adecuado de los objetivos financieros. Se recomienda mantener el control de gastos y optimizar las compras centralizadas para aprovechar descuentos por volumen.",
        }

