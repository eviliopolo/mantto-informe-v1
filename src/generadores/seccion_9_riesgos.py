"""
Generador Sección 9: Matriz de Riesgos
Tipo: 🟩 EXTRACCIÓN DATOS (riesgos, evaluación, mitigación)

Subsecciones:
- 9.1 Identificación de riesgos
- 9.2 Evaluación (Probabilidad, Impacto)
- 9.3 Matriz consolidada y clasificación
- 9.4 Medidas de tratamiento y plan de acción
- 9.5 Seguimiento e indicadores
"""
from pathlib import Path
from typing import Dict, Any, List
import json
import pandas as pd
import numpy as np
from .base import GeneradorSeccion
import config

# Intentar importar matplotlib, si no está disponible se manejará en el código
try:
    import matplotlib
    matplotlib.use('Agg')  # Backend sin GUI
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("[WARNING] matplotlib no está disponible. El gráfico heatmap no se generará.")


class GeneradorSeccion9(GeneradorSeccion):
    """Genera la sección 9: Matriz de Riesgos"""
    
    @property
    def nombre_seccion(self) -> str:
        return "9. MATRIZ DE RIESGOS"
    
    @property
    def template_file(self) -> str:
        return "seccion_9_riesgos.docx"
    
    def __init__(self, anio: int, mes: int):
        super().__init__(anio, mes)
        self.riesgos: List[Dict] = []
        self.resumen_clasificacion: List[Dict] = []
        self.grafico_matriz_img: str = ""
    
    def _calcular_clasificacion(self, nivel_num: int) -> str:
        """
        Mapea nivel numérico a clasificación textual
        
        Args:
            nivel_num: Nivel numérico (probabilidad × impacto)
        
        Returns:
            Clasificación: "Bajo", "Medio", "Alto", "Crítico"
        """
        if nivel_num <= 4:
            return "Bajo"
        elif nivel_num <= 8:
            return "Medio"
        elif nivel_num <= 12:
            return "Alto"
        else:  # 13-25
            return "Crítico"
    
    def _procesar_riesgos(self) -> None:
        """Procesa los riesgos: calcula nivel numérico, clasificación y ordena"""
        for riesgo in self.riesgos:
            probabilidad = riesgo.get("probabilidad", 1)
            impacto = riesgo.get("impacto", 1)
            nivel_num = probabilidad * impacto
            riesgo["nivel_num"] = nivel_num
            riesgo["clasificacion"] = self._calcular_clasificacion(nivel_num)
        
        # Ordenar por nivel_num descendente
        self.riesgos.sort(key=lambda x: x.get("nivel_num", 0), reverse=True)
    
    def _generar_resumen_clasificacion(self) -> None:
        """Genera resumen agregado por clasificación"""
        if not self.riesgos:
            self.resumen_clasificacion = []
            return
        
        # Contar por clasificación
        df = pd.DataFrame(self.riesgos)
        resumen = df.groupby('clasificacion').size().reset_index(name='cantidad')
        total = len(self.riesgos)
        
        self.resumen_clasificacion = []
        for _, row in resumen.iterrows():
            porcentaje = round((row['cantidad'] / total) * 100, 2)
            self.resumen_clasificacion.append({
                "clasificacion": row['clasificacion'],
                "cantidad": int(row['cantidad']),
                "porcentaje": porcentaje
            })
        
        # Ordenar por nivel de riesgo (Crítico > Alto > Medio > Bajo)
        orden = {"Crítico": 4, "Alto": 3, "Medio": 2, "Bajo": 1}
        self.resumen_clasificacion.sort(key=lambda x: orden.get(x["clasificacion"], 0), reverse=True)
    
    def _generar_heatmap(self, output_dir: Path) -> str:
        """
        Genera gráfico heatmap de la matriz de riesgos
        
        Args:
            output_dir: Directorio de salida
        
        Returns:
            Ruta al archivo PNG generado o cadena vacía si no se pudo generar
        """
        if not MATPLOTLIB_DISPONIBLE:
            return ""
        
        if not self.riesgos:
            return ""
        
        try:
            # Crear matriz 5x5 (probabilidad vs impacto)
            matriz = np.zeros((5, 5))
            
            for riesgo in self.riesgos:
                prob = riesgo.get("probabilidad", 1) - 1  # Convertir 1-5 a 0-4
                imp = riesgo.get("impacto", 1) - 1
                if 0 <= prob < 5 and 0 <= imp < 5:
                    matriz[imp, prob] += 1  # Impacto en filas, Probabilidad en columnas
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Crear heatmap
            im = ax.imshow(matriz, cmap='YlOrRd', aspect='auto', vmin=0, vmax=max(1, matriz.max()))
            
            # Etiquetas
            ax.set_xticks(range(5))
            ax.set_yticks(range(5))
            ax.set_xticklabels([str(i+1) for i in range(5)])
            ax.set_yticklabels([str(i+1) for i in range(5)])
            ax.set_xlabel('Probabilidad (1-5)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Impacto (1-5)', fontsize=12, fontweight='bold')
            ax.set_title('Matriz de Riesgos - Probabilidad vs Impacto', fontsize=14, fontweight='bold')
            
            # Agregar valores en las celdas
            for i in range(5):
                for j in range(5):
                    if matriz[i, j] > 0:
                        text = ax.text(j, i, int(matriz[i, j]),
                                     ha="center", va="center", color="black", fontweight='bold')
            
            # Agregar barra de color
            plt.colorbar(im, ax=ax, label='Cantidad de Riesgos')
            
            # Agregar líneas de clasificación
            # Línea Bajo/Medio (nivel 4)
            ax.plot([-0.5, 4.5], [3.5, 3.5], 'b--', alpha=0.3, linewidth=1)
            ax.plot([3.5, 3.5], [-0.5, 4.5], 'b--', alpha=0.3, linewidth=1)
            
            # Línea Medio/Alto (nivel 8)
            ax.plot([-0.5, 4.5], [1.5, 1.5], 'orange', linestyle='--', alpha=0.3, linewidth=1)
            ax.plot([1.5, 1.5], [-0.5, 4.5], 'orange', linestyle='--', alpha=0.3, linewidth=1)
            
            # Leyenda de clasificación
            legend_elements = [
                mpatches.Patch(color='lightblue', label='Bajo (1-4)'),
                mpatches.Patch(color='yellow', label='Medio (5-8)'),
                mpatches.Patch(color='orange', label='Alto (9-12)'),
                mpatches.Patch(color='red', label='Crítico (13-25)')
            ]
            ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.15, 1))
            
            plt.tight_layout()
            
            # Guardar
            output_path = output_dir / "matriz_riesgos_heatmap.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return str(output_path)
        except Exception as e:
            print(f"[WARNING] Error al generar heatmap: {e}")
            return ""
    
    def cargar_datos(self) -> None:
        """Carga datos de la sección 9 desde CSV o genera datos dummy"""
        # Intentar cargar desde archivo CSV
        archivo_csv = config.FUENTES_DIR / "matriz_riesgos.csv"
        
        datos_cargados = False
        
        if archivo_csv.exists():
            try:
                df = pd.read_csv(archivo_csv, encoding='utf-8')
                # Convertir DataFrame a lista de diccionarios
                self.riesgos = df.to_dict('records')
                datos_cargados = True
                print(f"[INFO] Datos cargados desde CSV: {archivo_csv}")
            except Exception as e:
                print(f"[WARNING] Error al cargar CSV {archivo_csv}: {e}")
        
        # Si no hay datos, generar dummy
        if not datos_cargados:
            print(f"[INFO] No se encontraron fuentes de datos, generando datos dummy para pruebas")
            self._generar_datos_dummy()
            self._guardar_csv_demo()
        
        # Procesar riesgos (calcular niveles y clasificaciones)
        self._procesar_riesgos()
        self._generar_resumen_clasificacion()
    
    def _generar_datos_dummy(self) -> None:
        """Genera datos dummy para pruebas cuando no hay fuentes externas"""
        mes_nombre = config.MESES[self.mes]
        
        self.riesgos = [
            {
                "id": 1,
                "riesgo": "Fallas eléctricas masivas",
                "probabilidad": 3,
                "impacto": 5,
                "descripcion": "Cortes de energía que afectan centros de monitoreo y sistemas críticos",
                "mitigacion": "Instalación UPS adicional y pruebas de respaldo energético",
                "responsable": "Coordinación Técnica",
                "fecha_compromiso": f"2025-{self.mes:02d}-05"
            },
            {
                "id": 2,
                "riesgo": "Vandalismo en cámaras exteriores",
                "probabilidad": 4,
                "impacto": 3,
                "descripcion": "Daños físicos a cámaras que reducen cobertura y calidad de grabación",
                "mitigacion": "Refuerzo de carcasa protectora y patrullaje preventivo",
                "responsable": "Seguridad Operativa",
                "fecha_compromiso": f"2025-{self.mes:02d}-30"
            },
            {
                "id": 3,
                "riesgo": "Falla masiva de conectividad de red",
                "probabilidad": 2,
                "impacto": 5,
                "descripcion": "Interrupción de servicios de red que impide transmisión de video",
                "mitigacion": "Redundancia de enlaces y monitoreo proactivo",
                "responsable": "Coordinación Técnica",
                "fecha_compromiso": f"2025-{self.mes+1:02d}-10" if self.mes < 12 else f"2026-01-10"
            },
            {
                "id": 4,
                "riesgo": "Robo de equipos en campo",
                "probabilidad": 3,
                "impacto": 4,
                "descripcion": "Sustracción de equipos de red y cámaras en ubicaciones vulnerables",
                "mitigacion": "Seguridad física mejorada y sistemas de alerta",
                "responsable": "Seguridad Operativa",
                "fecha_compromiso": f"2025-{self.mes:02d}-25"
            },
            {
                "id": 5,
                "riesgo": "Desgaste prematuro de componentes",
                "probabilidad": 4,
                "impacto": 2,
                "descripcion": "Falla anticipada de componentes por condiciones ambientales adversas",
                "mitigacion": "Mantenimiento preventivo intensificado y reemplazo programado",
                "responsable": "Brigada de Mantenimiento",
                "fecha_compromiso": f"2025-{self.mes:02d}-20"
            },
            {
                "id": 6,
                "riesgo": "Incapacidad de personal clave",
                "probabilidad": 2,
                "impacto": 4,
                "descripcion": "Ausencia prolongada de técnicos especializados afecta operación",
                "mitigacion": "Capacitación cruzada y documentación de procedimientos",
                "responsable": "Recursos Humanos",
                "fecha_compromiso": f"2025-{self.mes+1:02d}-15" if self.mes < 12 else f"2026-01-15"
            }
        ]
    
    def _guardar_csv_demo(self) -> None:
        """Guarda un CSV de ejemplo con los datos dummy generados"""
        try:
            df = pd.DataFrame(self.riesgos)
            csv_demo = config.FUENTES_DIR / "matriz_riesgos_demo.csv"
            df.to_csv(csv_demo, index=False, encoding='utf-8')
            print(f"[INFO] CSV de ejemplo guardado en: {csv_demo}")
        except Exception as e:
            print(f"[WARNING] No se pudo guardar CSV de ejemplo: {e}")
    
    def procesar(self) -> Dict[str, Any]:
        """Procesa y retorna el contexto para el template"""
        total_riesgos = len(self.riesgos)
        riesgos_criticos = sum(1 for r in self.riesgos if r.get("clasificacion") == "Crítico")
        riesgos_altos = sum(1 for r in self.riesgos if r.get("clasificacion") == "Alto")
        
        # Generar narrativa
        if total_riesgos > 0:
            narrativa = f"Se identificaron {total_riesgos} riesgos en el periodo. Se priorizan los riesgos de nivel CRÍTICO ({riesgos_criticos}) y ALTO ({riesgos_altos}) para acciones inmediatas."
        else:
            narrativa = "No se identificaron riesgos para el periodo reportado."
        
        return {
            # Narrativa
            "texto_intro": narrativa,
            
            # 9.1-9.3 Lista de riesgos completa
            "riesgos": self.riesgos,
            "total_riesgos": total_riesgos,
            "hay_riesgos": total_riesgos > 0,
            
            # 9.3 Resumen por clasificación
            "resumen_clasificacion": self.resumen_clasificacion,
            "total_resumen": len(self.resumen_clasificacion),
            "hay_resumen": len(self.resumen_clasificacion) > 0,
            
            # Placeholder para gráfico
            "grafico_matriz_img": self.grafico_matriz_img,
            
            # Estadísticas adicionales
            "riesgos_criticos": riesgos_criticos,
            "riesgos_altos": riesgos_altos,
            "riesgos_medios": sum(1 for r in self.riesgos if r.get("clasificacion") == "Medio"),
            "riesgos_bajos": sum(1 for r in self.riesgos if r.get("clasificacion") == "Bajo"),
        }
    
    def generar(self) -> Any:
        """Genera la sección completa, incluyendo el gráfico"""
        # Generar heatmap antes de procesar
        output_dir = config.OUTPUT_DIR / f"{self.anio}" / f"{self.mes:02d}_{config.MESES[self.mes]}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.grafico_matriz_img = self._generar_heatmap(output_dir)
        
        # Llamar al método generar de la clase base
        return super().generar()

