"""
Servicio para conexión y lectura de archivos Excel desde SharePoint
Especializado para extraer datos de la sección 2.5 (Escalamientos)
"""
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
import logging
import os
from src.extractores.sharepoint_extractor import SharePointExtractor
import config

logger = logging.getLogger(__name__)


class SharePointService:
    """Servicio para manejar conexión y lectura de archivos desde SharePoint"""
    
    def __init__(self):
        """Inicializa el servicio con el extractor de SharePoint"""
        # Obtener credenciales de SharePoint desde config (que ya carga del .env)
        # Siguiendo el patrón de seccion_1_info_general.py
        sharepoint_site_url = getattr(config, 'SHAREPOINT_SITE_URL', None) or os.getenv("SHAREPOINT_SITE_URL")
        sharepoint_client_id = getattr(config, 'SHAREPOINT_CLIENT_ID', None) or os.getenv("SHAREPOINT_CLIENT_ID")
        sharepoint_client_secret = getattr(config, 'SHAREPOINT_CLIENT_SECRET', None) or os.getenv("SHAREPOINT_CLIENT_SECRET")
        sharepoint_tenant_id = getattr(config, 'SHAREPOINT_TENANT_ID', None) or os.getenv("SHAREPOINT_TENANT_ID")
        sharepoint_base_path = getattr(config, 'SHAREPOINT_BASE_PATH', None) or os.getenv("SHAREPOINT_BASE_PATH")
        
        # Inicializar extractor con credenciales
        self.extractor = SharePointExtractor(
            site_url=sharepoint_site_url,
            client_id=sharepoint_client_id,
            client_secret=sharepoint_client_secret,
            tenant_id=sharepoint_tenant_id,
            base_path=sharepoint_base_path
        )
    
    async def leer_excel_desde_sharepoint(
        self,
        ruta_sharepoint: str,
        hojas: Optional[List[str]] = None,
        indices_hojas: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Lee un archivo Excel desde SharePoint y extrae datos de hojas específicas.
        
        Args:
            ruta_sharepoint: Ruta del archivo Excel en SharePoint
                          Puede ser URL completa o ruta relativa
            hojas: Lista de nombres de hojas a leer (ej: ["Hoja1", "Escalamientos"])
            indices_hojas: Lista de índices de hojas a leer (ej: [0, 1, 2])
                          Si se proporciona, se usa en lugar de hojas
                          
        Returns:
            Diccionario con:
            {
                "success": bool,
                "message": str,
                "datos": {
                    "hoja1": DataFrame o lista de diccionarios,
                    "hoja2": DataFrame o lista de diccionarios,
                    ...
                },
                "hojas_disponibles": List[str]
            }
        """
        archivo_temp = None
        
        try:
            # Descargar archivo desde SharePoint
            logger.info(f"Descargando archivo Excel desde SharePoint: {ruta_sharepoint}")
            archivo_temp = self.extractor.descargar_archivo(ruta_sharepoint)
            
            if not archivo_temp or not archivo_temp.exists():
                return {
                    "success": False,
                    "message": f"No se pudo descargar el archivo desde SharePoint: {ruta_sharepoint}",
                    "datos": {},
                    "hojas_disponibles": []
                }
            
            logger.info(f"Archivo descargado exitosamente: {archivo_temp}")
            
            # Leer todas las hojas disponibles primero
            try:
                excel_file = pd.ExcelFile(archivo_temp)
                hojas_disponibles = excel_file.sheet_names
                logger.info(f"Hojas disponibles en el Excel: {hojas_disponibles}")
            except Exception as e:
                logger.error(f"Error al leer el archivo Excel: {e}")
                return {
                    "success": False,
                    "message": f"Error al leer el archivo Excel: {str(e)}",
                    "datos": {},
                    "hojas_disponibles": []
                }
            
            # Determinar qué hojas leer
            hojas_a_leer = []
            
            if indices_hojas:
                # Leer por índices
                for idx in indices_hojas:
                    if 0 <= idx < len(hojas_disponibles):
                        hojas_a_leer.append((idx, hojas_disponibles[idx]))
                    else:
                        logger.warning(f"Índice de hoja {idx} fuera de rango. Hojas disponibles: {len(hojas_disponibles)}")
            elif hojas:
                # Leer por nombres
                for nombre_hoja in hojas:
                    if nombre_hoja in hojas_disponibles:
                        idx = hojas_disponibles.index(nombre_hoja)
                        hojas_a_leer.append((idx, nombre_hoja))
                    else:
                        logger.warning(f"Hoja '{nombre_hoja}' no encontrada. Hojas disponibles: {hojas_disponibles}")
            else:
                # Leer todas las hojas
                hojas_a_leer = [(idx, nombre) for idx, nombre in enumerate(hojas_disponibles)]
            
            if not hojas_a_leer:
                return {
                    "success": False,
                    "message": "No se encontraron hojas para leer",
                    "datos": {},
                    "hojas_disponibles": hojas_disponibles
                }
            
            # Leer cada hoja solicitada
            datos_hojas = {}
            
            for idx, nombre_hoja in hojas_a_leer:
                try:
                    logger.info(f"Leyendo hoja '{nombre_hoja}' (índice {idx})...")
                    df = pd.read_excel(archivo_temp, sheet_name=idx)
                    
                    if df.empty:
                        logger.warning(f"La hoja '{nombre_hoja}' está vacía")
                        datos_hojas[nombre_hoja] = []
                    else:
                        # Convertir DataFrame a lista de diccionarios
                        # Reemplazar NaN por None y limpiar datos
                        df_limpio = df.fillna("")
                        
                        # Convertir Timestamps de pandas a strings antes de convertir a dict
                        # Esto evita que las fechas se conviertan a formato datetime completo
                        for col in df_limpio.columns:
                            if df_limpio[col].dtype == 'datetime64[ns]':
                                # Convertir fechas a formato string YYYY-MM-DD para facilitar el formateo posterior
                                df_limpio[col] = df_limpio[col].dt.strftime('%Y-%m-%d')
                        
                        datos_hojas[nombre_hoja] = df_limpio.to_dict('records')
                        logger.info(f"Hoja '{nombre_hoja}': {len(datos_hojas[nombre_hoja])} filas leídas")
                
                except Exception as e:
                    logger.error(f"Error al leer la hoja '{nombre_hoja}': {e}")
                    datos_hojas[nombre_hoja] = []
            
            return {
                "success": True,
                "message": f"Archivo leído exitosamente. {len(hojas_a_leer)} hoja(s) procesada(s)",
                "datos": datos_hojas,
                "hojas_disponibles": hojas_disponibles
            }
            
        except Exception as e:
            logger.error(f"Error general al leer Excel desde SharePoint: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error al leer Excel desde SharePoint: {str(e)}",
                "datos": {},
                "hojas_disponibles": []
            }
        
        finally:
            # Limpiar archivo temporal
            if archivo_temp and archivo_temp.exists():
                try:
                    archivo_temp.unlink()
                    logger.debug(f"Archivo temporal eliminado: {archivo_temp}")
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal {archivo_temp}: {e}")
    
    async def leer_excel_escalamientos(
        self,
        ruta_sharepoint: str,
        nombre_hoja: Optional[str] = None,
        indice_hoja: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Método específico para leer datos de escalamientos desde Excel.
        Extrae datos de una hoja específica y los formatea para la tabla de la sección 2.5.
        
        Args:
            ruta_sharepoint: Ruta del archivo Excel en SharePoint
            nombre_hoja: Nombre de la hoja a leer (opcional)
            indice_hoja: Índice de la hoja a leer (opcional, si no se especifica nombre_hoja)
            
        Returns:
            Lista de diccionarios con los datos de escalamientos formateados
        """
        # Determinar qué hojas leer
        if nombre_hoja:
            hojas = [nombre_hoja]
            indices_hojas = None
        elif indice_hoja is not None:
            hojas = None
            indices_hojas = [indice_hoja]
        else:
            # Por defecto, leer la primera hoja
            hojas = None
            indices_hojas = [0]
        
        # Leer el Excel
        resultado = await self.leer_excel_desde_sharepoint(
            ruta_sharepoint=ruta_sharepoint,
            hojas=hojas,
            indices_hojas=indices_hojas
        )
        
        if not resultado.get("success"):
            logger.error(f"Error al leer Excel de escalamientos: {resultado.get('message')}")
            return []
        
        # Obtener los datos de la primera hoja leída
        datos_hojas = resultado.get("datos", {})
        
        if not datos_hojas:
            logger.warning("No se encontraron datos en las hojas leídas")
            return []
        
        # Retornar los datos de la primera hoja encontrada
        primera_hoja = list(datos_hojas.keys())[0]
        datos = datos_hojas[primera_hoja]
        
        logger.info(f"Datos de escalamientos extraídos: {len(datos)} registros desde la hoja '{primera_hoja}'")
        
        return datos
    
    async def leer_excel_escalamientos_completo(
        self,
        ruta_textual: str,
        ruta_base: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lee un archivo Excel con 3 hojas desde SharePoint y extrae datos para las secciones 2.5.1, 2.5.2, 2.5.3.
        También genera un consolidado para la sección 2.5.
        
        Args:
            ruta_textual: Ruta textual del archivo Excel (se concatena con ruta_base)
            ruta_base: Ruta base de SharePoint (opcional, si no se proporciona se usa desde config)
            
        Returns:
            Diccionario con:
            {
                "success": bool,
                "message": str,
                "datos": {
                    "enel": List[Dict],  # Hoja 1 -> Sección 2.5.1
                    "caida_masiva": List[Dict],  # Hoja 2 -> Sección 2.5.2
                    "conectividad": List[Dict],  # Hoja 3 -> Sección 2.5.3
                    "consolidado": List[Dict]  # Sumatoria de las 3 hojas -> Sección 2.5
                }
            }
        """
        try:
            # Construir ruta completa
            # Si ruta_textual es una URL completa (empieza con http:// o https://), usarla directamente sin ruta_base
            if ruta_textual.startswith("http://") or ruta_textual.startswith("https://"):
                ruta_completa = ruta_textual
                logger.info(f"Ruta textual es URL completa, usando directamente (sin ruta_base): {ruta_completa}")
            elif ruta_base:
                # Si hay ruta_base y no es URL completa, concatenar
                ruta_completa = f"{ruta_base.rstrip('/')}/{ruta_textual.lstrip('/')}"
            else:
                # Usar ruta textual directamente (debe ser ruta relativa del servidor)
                ruta_completa = ruta_textual
            
            logger.info(f"Leyendo Excel de escalamientos desde: {ruta_completa}")
            
            # Leer las 3 primeras hojas del Excel
            resultado = await self.leer_excel_desde_sharepoint(
                ruta_sharepoint=ruta_completa,
                indices_hojas=[0, 1, 2]  # Leer las primeras 3 hojas
            )
            
            if not resultado.get("success"):
                return {
                    "success": False,
                    "message": resultado.get("message", "Error al leer el archivo Excel"),
                    "datos": {
                        "enel": [],
                        "caida_masiva": [],
                        "conectividad": [],
                        "consolidado": []
                    }
                }
            
            datos_hojas = resultado.get("datos", {})
            hojas_disponibles = resultado.get("hojas_disponibles", [])
            
            # Extraer datos de cada hoja
            # Orden en el Excel: CAIDA MASIVA (hoja 1), CONECTIVIDAD (hoja 2), ENEL (hoja 3)
            datos_enel = []
            datos_caida_masiva = []
            datos_conectividad = []
            
            # Asignar datos según el índice de la hoja
            # Hoja 1 = CAIDA MASIVA
            if len(hojas_disponibles) > 0:
                hoja_1 = hojas_disponibles[0]
                datos_caida_masiva = datos_hojas.get(hoja_1, [])
                logger.info(f"Hoja 1 ({hoja_1}): {len(datos_caida_masiva)} registros para CAÍDA MASIVA")
            
            # Hoja 2 = CONECTIVIDAD
            if len(hojas_disponibles) > 1:
                hoja_2 = hojas_disponibles[1]
                datos_conectividad = datos_hojas.get(hoja_2, [])
                logger.info(f"Hoja 2 ({hoja_2}): {len(datos_conectividad)} registros para CONECTIVIDAD")
            
            # Hoja 3 = ENEL
            if len(hojas_disponibles) > 2:
                hoja_3 = hojas_disponibles[2]
                datos_enel = datos_hojas.get(hoja_3, [])
                logger.info(f"Hoja 3 ({hoja_3}): {len(datos_enel)} registros para ENEL")
            
            # Generar consolidado (sumatoria de las 3 hojas)
            # El consolidado puede ser simplemente la unión de todas las filas
            # o una sumatoria según los campos numéricos
            consolidado = []
            
            # Opción 1: Unir todas las filas con un campo que indique el tipo
            for registro in datos_enel:
                registro_con_tipo = registro.copy()
                registro_con_tipo["tipo"] = "ENEL"
                consolidado.append(registro_con_tipo)
            
            for registro in datos_caida_masiva:
                registro_con_tipo = registro.copy()
                registro_con_tipo["tipo"] = "CAÍDA MASIVA"
                consolidado.append(registro_con_tipo)
            
            for registro in datos_conectividad:
                registro_con_tipo = registro.copy()
                registro_con_tipo["tipo"] = "CONECTIVIDAD"
                consolidado.append(registro_con_tipo)
            
            logger.info(f"Consolidado generado: {len(consolidado)} registros totales")
            
            return {
                "success": True,
                "message": f"Excel leído exitosamente. {len(hojas_disponibles)} hoja(s) procesada(s)",
                "datos": {
                    "enel": datos_enel,
                    "caida_masiva": datos_caida_masiva,
                    "conectividad": datos_conectividad,
                    "consolidado": consolidado
                }
            }
            
        except Exception as e:
            logger.error(f"Error al leer Excel de escalamientos completo: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error al leer Excel de escalamientos: {str(e)}",
                "datos": {
                    "enel": [],
                    "caida_masiva": [],
                    "conectividad": [],
                    "consolidado": []
                }
            }


# Instancia global del servicio
_sharepoint_service_instance: Optional[SharePointService] = None


async def get_sharepoint_service() -> SharePointService:
    """Obtiene la instancia singleton del servicio de SharePoint"""
    global _sharepoint_service_instance
    if _sharepoint_service_instance is None:
        _sharepoint_service_instance = SharePointService()
    return _sharepoint_service_instance

