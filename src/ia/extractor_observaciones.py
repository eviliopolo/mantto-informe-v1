"""
Extractor de observaciones desde archivos de anexos usando LLM
"""
from typing import Dict, Optional, List
from pathlib import Path
import os
import tempfile
import config
from src.extractores.sharepoint_extractor import get_sharepoint_extractor

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Intentar importar OpenAI
try:
    from openai import OpenAI
    OPENAI_DISPONIBLE = True
except ImportError:
    OPENAI_DISPONIBLE = False
    print("[WARNING] openai no está disponible. Las observaciones se generarán de forma estática.")

# Intentar importar otras librerías para lectura de PDFs
try:
    import PyPDF2
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

try:
    from docx import Document as DocxDocument
    DOCX_DISPONIBLE = True
except ImportError:
    DOCX_DISPONIBLE = False


class ExtractorObservaciones:
    """Extrae observaciones de cumplimiento desde archivos de anexos usando LLM"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini",
                 sharepoint_site_url: Optional[str] = None, sharepoint_client_id: Optional[str] = None,
                 sharepoint_client_secret: Optional[str] = None, sharepoint_base_path: Optional[str] = None):
        """
        Inicializa el extractor de observaciones
        
        Args:
            api_key: API key de OpenAI (o usar variable de entorno OPENAI_API_KEY)
            model: Modelo de OpenAI a usar (default: gpt-4o-mini)
            sharepoint_site_url: URL del sitio de SharePoint
            sharepoint_client_id: Client ID para autenticación de aplicación
            sharepoint_client_secret: Client Secret para autenticación de aplicación
            sharepoint_base_path: Ruta base adicional en SharePoint (ej: "Documentos compartidos")
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or getattr(config, 'OPENAI_API_KEY', None)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini") or getattr(config, 'OPENAI_MODEL', "gpt-4o-mini")
        self.client = None
        
        if OPENAI_DISPONIBLE and self.api_key:
            try:
                # Inicializar cliente OpenAI - usar variable de entorno si está disponible
                # o pasar api_key explícitamente
                if os.getenv("OPENAI_API_KEY"):
                    # Si está en variable de entorno, OpenAI() la detecta automáticamente
                    self.client = OpenAI()
                else:
                    # Si no está en variable de entorno, pasarla explícitamente
                    self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"[WARNING] Error al inicializar cliente OpenAI: {e}")
                print(f"[INFO] Intentando con configuración alternativa...")
                try:
                    # Intentar solo con variable de entorno
                    self.client = OpenAI()
                except Exception as e2:
                    print(f"[WARNING] Error al inicializar cliente OpenAI (fallback): {e2}")
                    self.client = None
        
        # Inicializar extractor de SharePoint
        self.sharepoint_extractor = get_sharepoint_extractor(
            site_url=sharepoint_site_url,
            client_id=sharepoint_client_id,
            client_secret=sharepoint_client_secret,
            base_path=sharepoint_base_path
        )
        self.archivos_temporales = []  # Para limpiar archivos descargados
        self.cache_archivos_descargados = {}  # Cache de archivos descargados por ruta normalizada
    
    def extraer_texto_archivo(self, ruta_archivo: str) -> str:
        """
        Extrae texto de un archivo (PDF, DOCX, TXT)
        Soporta archivos locales y desde SharePoint
        
        Args:
            ruta_archivo: Ruta al archivo (local, Path, o URL de SharePoint)
            
        Returns:
            Texto extraído del archivo
        """
        # Si es Path, convertir a string
        if isinstance(ruta_archivo, Path):
            ruta_archivo = str(ruta_archivo)
        
        # Verificar si es un archivo temporal ya descargado (no volver a descargar)
        if isinstance(ruta_archivo, str):
            ruta_path = Path(ruta_archivo)
            # Si el archivo existe localmente y está en el directorio temporal, ya fue descargado
            if ruta_path.exists() and str(ruta_path.parent).startswith(str(Path(tempfile.gettempdir()))):
                print(f"[DEBUG] Archivo ya descargado, extrayendo texto directamente...")
                # Continuar con la extracción local (no descargar nuevamente)
            # Verificar si es URL de SharePoint (solo URLs completas, no rutas relativas del servidor)
            elif self.sharepoint_extractor.es_url_sharepoint(ruta_archivo):
                print(f"[DEBUG] Detectada URL de SharePoint, descargando...")
                return self._extraer_texto_desde_sharepoint(ruta_archivo)
            # Verificar si es ruta relativa del servidor (comienza con /sites/, /teams/, etc.)
            elif ruta_archivo.startswith('/sites/') or ruta_archivo.startswith('/teams/') or ruta_archivo.startswith('/personal/'):
                print(f"[DEBUG] Detectada ruta relativa del servidor, descargando desde SharePoint...")
                return self._extraer_texto_desde_sharepoint(ruta_archivo)
        
        # Convertir a Path si es string
        if isinstance(ruta_archivo, str):
            ruta_archivo = Path(ruta_archivo)
        
        if not ruta_archivo.exists():
            print(f"[WARNING] Archivo no existe: {ruta_archivo}")
            return ""
        
        extension = ruta_archivo.suffix.lower()
        print(f"[DEBUG] Extrayendo texto de archivo local: {ruta_archivo} (extensión: {extension})")
        
        try:
            if extension == '.pdf' and PDF_DISPONIBLE:
                texto = self._leer_pdf(ruta_archivo)
                print(f"[DEBUG] Texto extraído de PDF: {len(texto)} caracteres")
                return texto
            elif extension in ['.docx', '.doc'] and DOCX_DISPONIBLE:
                texto = self._leer_docx(ruta_archivo)
                print(f"[DEBUG] Texto extraído de DOCX: {len(texto)} caracteres")
                return texto
            elif extension == '.txt':
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
                print(f"[DEBUG] Texto extraído de TXT: {len(texto)} caracteres")
                return texto
            else:
                print(f"[WARNING] Formato no soportado: {extension}")
                return ""
        except Exception as e:
            print(f"[WARNING] Error al leer archivo {ruta_archivo}: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _extraer_texto_desde_sharepoint(self, url_sharepoint: str) -> str:
        """
        Extrae texto de un archivo desde SharePoint
        
        Args:
            url_sharepoint: URL del archivo en SharePoint o ruta relativa del servidor
            
        Returns:
            Texto extraído del archivo
        """
        print(f"[INFO] Descargando archivo desde SharePoint: {url_sharepoint}")
        print(f"[DEBUG] Tipo de ruta: {'URL completa' if url_sharepoint.startswith('http') else 'Ruta relativa del servidor'}")
        
        # Descargar archivo temporalmente
        try:
            archivo_temp = self.sharepoint_extractor.descargar_archivo(url_sharepoint)
        except Exception as e:
            print(f"[ERROR] Error al descargar archivo desde SharePoint: {e}")
            import traceback
            traceback.print_exc()
            return ""
        
        if not archivo_temp:
            print(f"[WARNING] No se pudo descargar archivo desde SharePoint (retornó None): {url_sharepoint}")
            return ""
        
        if not archivo_temp.exists():
            print(f"[WARNING] Archivo descargado no existe: {archivo_temp}")
            return ""
        
        tamaño = archivo_temp.stat().st_size
        print(f"[INFO] Archivo descargado exitosamente: {archivo_temp} (tamaño: {tamaño} bytes)")
        
        if tamaño == 0:
            print(f"[WARNING] El archivo descargado está vacío (0 bytes)")
            return ""
        
        # Guardar referencia para limpiar después
        self.archivos_temporales.append(archivo_temp)
        
        # Extraer texto del archivo descargado
        try:
            # Pasar como Path, no como string, para que se lea como archivo local
            texto = self.extraer_texto_archivo(str(archivo_temp))
            print(f"[INFO] Texto extraído del archivo: {len(texto)} caracteres")
            if len(texto) > 0:
                print(f"[DEBUG] Primeros 200 caracteres del texto: {texto[:200]}...")
            else:
                print(f"[WARNING] No se pudo extraer texto del archivo (archivo puede estar corrupto o ser imagen)")
            return texto
        except Exception as e:
            print(f"[ERROR] Error al extraer texto del archivo: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _leer_pdf(self, ruta: Path) -> str:
        """Lee texto de un archivo PDF"""
        texto = ""
        try:
            with open(ruta, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    texto += page.extract_text() + "\n"
        except Exception as e:
            print(f"[WARNING] Error al leer PDF {ruta}: {e}")
        return texto
    
    def _leer_docx(self, ruta: Path) -> str:
        """Lee texto de un archivo DOCX"""
        texto = ""
        try:
            doc = DocxDocument(ruta)
            for para in doc.paragraphs:
                texto += para.text + "\n"
        except Exception as e:
            print(f"[WARNING] Error al leer DOCX {ruta}: {e}")
        return texto
    
    def generar_observacion_llm(self, texto_anexo: str, obligacion: str, 
                                periodicidad: str, cumplio: str,
                                informes_aprobados_contexto: Optional[List[str]] = None) -> str:
        """
        Genera observación de cumplimiento usando LLM basándose en el contenido del anexo
        y los últimos informes aprobados como contexto
        
        Args:
            texto_anexo: Texto extraído del archivo de anexo
            obligacion: Texto de la obligación
            periodicidad: Periodicidad de la obligación
            cumplio: Estado de cumplimiento ("Cumplió" o "No Cumplió")
            informes_aprobados_contexto: Lista de textos extraídos de los últimos 3 informes aprobados (opcional)
            
        Returns:
            Observación generada
        """
        if not self.client or not OPENAI_DISPONIBLE:
            # Fallback: retornar observación genérica
            return self._generar_observacion_fallback(obligacion, cumplio)
        
        if not texto_anexo or len(texto_anexo.strip()) < 50:
            # Si el texto es muy corto, usar fallback
            return self._generar_observacion_fallback(obligacion, cumplio)
        
        try:
            # Construir contexto de informes aprobados con énfasis en observaciones específicas
            contexto_informes = ""
            if informes_aprobados_contexto:
                contexto_informes = "\n\n═══════════════════════════════════════════════════════════\n"
                contexto_informes += "OBSERVACIONES DE INFORMES APROBADOS ANTERIORES (REFERENCIA PRINCIPAL):\n"
                contexto_informes += "═══════════════════════════════════════════════════════════\n"
                contexto_informes += "IMPORTANTE: Estas son las observaciones REALES y APROBADAS de la MISMA SECCIÓN de meses anteriores.\n"
                contexto_informes += "Estas observaciones provienen de la misma sección del informe (1.5.1, 1.5.2 o 1.5.3 según corresponda).\n"
                contexto_informes += "DEBES generar una observación CASI IDÉNTICA en tono, estilo, estructura y terminología.\n"
                contexto_informes += "MANTÉN el mismo tono de redacción, las mismas expresiones técnicas y el mismo estilo de escritura.\n"
                contexto_informes += "Usa estas observaciones como PLANTILLA EXACTA y solo adapta detalles específicos del anexo actual.\n"
                contexto_informes += "NO cambies el tono, las frases clave ni la estructura general.\n\n"
                
                for i, texto_informe in enumerate(informes_aprobados_contexto[:3], 1):
                    # Extraer la sección relevante de cada informe (puede ser 1.5.1, 1.5.2 o 1.5.3)
                    # Aumentar límite para capturar más contexto de observaciones
                    texto_limite = texto_informe[:4000] if len(texto_informe) > 4000 else texto_informe
                    contexto_informes += f"--- OBSERVACIONES DEL INFORME APROBADO {i} (MES ANTERIOR - MISMA SECCIÓN) ---\n"
                    contexto_informes += f"{texto_limite}\n"
                    contexto_informes += f"--- FIN OBSERVACIONES INFORME {i} ---\n\n"
            
            prompt = f"""Eres un asistente experto en generar observaciones de cumplimiento contractual para informes técnicos. Tu objetivo principal es mantener la CONSISTENCIA y SIMILITUD EXACTA con las observaciones de informes aprobados anteriores de la MISMA SECCIÓN.

CONTEXTO DE LA OBLIGACIÓN:
- Obligación: {obligacion}
- Periodicidad: {periodicidad}
- Estado: {cumplio}
{contexto_informes}

CONTENIDO DEL ANEXO ACTUAL:
{texto_anexo[:4000]}

INSTRUCCIONES CRÍTICAS (ORDEN DE PRIORIDAD):

1. **PRIORIDAD MÁXIMA - SIMILITUD EXACTA CON OBSERVACIONES DE LA MISMA SECCIÓN:**
   - Las observaciones anteriores provienen de la MISMA SECCIÓN del informe (1.5.1, 1.5.2 o 1.5.3)
   - DEBES generar una observación CASI IDÉNTICA en tono, estilo, estructura y terminología
   - MANTÉN el MISMO TONO de redacción que caracteriza a esta sección específica
   - Usa las MISMAS frases, expresiones técnicas y palabras clave que aparecen en los informes anteriores
   - Conserva el MISMO ESTILO de escritura (oraciones largas/cortas, uso de comas, estructura de párrafos)
   - Solo adapta detalles específicos del anexo actual si son relevantes y no cambian el sentido general
   - La observación debe ser RECONOCIBLE como parte de la misma serie de informes y de la misma sección

2. **CONSISTENCIA DE TONO POR SECCIÓN:**
   - Cada sección (1.5.1, 1.5.2, 1.5.3) tiene su propio tono y estilo característico
   - MANTÉN el tono específico de la sección a la que pertenece esta obligación
   - No mezcles estilos de diferentes secciones
   - Respeta las convenciones de redacción propias de esta sección

3. **CONSISTENCIA DE ESTILO:**
   - Mantén el mismo nivel de formalidad y profesionalismo
   - Usa la misma estructura de párrafos y longitud aproximada
   - Conserva las mismas palabras clave y expresiones técnicas
   - Respeta el mismo formato de redacción (oraciones largas/cortas, uso de comas, etc.)

4. **REFERENCIA AL ANEXO ACTUAL:**
   - Si las observaciones anteriores mencionan detalles específicos del anexo, adapta esos detalles al anexo actual
   - Mantén la misma forma de referenciar el anexo (ej: "según se detalla en el anexo actual", "conforme se evidencia en el anexo", etc.)
   - No cambies la estructura solo porque el anexo actual tenga información diferente

5. **REQUISITOS TÉCNICOS:**
   - Máximo 200 palabras
   - Texto corrido, sin viñetas ni listas
   - Lenguaje profesional y técnico apropiado para informes contractuales
   - Confirmar el cumplimiento de la obligación

IMPORTANTE: Si hay observaciones anteriores disponibles de la misma sección, tu objetivo es generar una observación que sea CASI IDÉNTICA en tono, estilo, estructura y terminología. La similitud con el tono de la sección es más importante que la creatividad. Solo adapta los detalles específicos del anexo actual cuando sea absolutamente necesario.

OBSERVACIÓN:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en redacción de informes técnicos y contractuales. Tu función principal es mantener la CONSISTENCIA y SIMILITUD con observaciones de informes anteriores. Priorizas la similitud sobre la creatividad."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1  # Temperatura muy baja para máxima consistencia y similitud con observaciones anteriores
            )
            
            observacion = response.choices[0].message.content.strip()
            return observacion
            
        except Exception as e:
            print(f"[WARNING] Error al generar observación con LLM: {e}")
            return self._generar_observacion_fallback(obligacion, cumplio)
    
    def extraer_fecha_y_asunto_comunicado(self, texto_archivo: str) -> Dict[str, Optional[str]]:
        """
        Extrae la fecha del encabezado y el asunto de un comunicado usando LLM
        
        Args:
            texto_archivo: Texto extraído del archivo del comunicado
        
        Returns:
            Diccionario con:
            {
                "fecha": "DD/MM/YYYY" o None,
                "asunto": "Texto del asunto" o None
            }
        """
        if not self.client or not OPENAI_DISPONIBLE:
            return {"fecha": None, "asunto": None}
        
        if not texto_archivo or len(texto_archivo.strip()) < 50:
            return {"fecha": None, "asunto": None}
        
        try:
            # Limitar texto a 8000 caracteres para asegurar que capture el encabezado completo
            texto_limitado = texto_archivo[:8000]
            
            print(f"[DEBUG] ========== EXTRACCIÓN FECHA Y ASUNTO CON LLM ==========")
            print(f"[DEBUG] Longitud del texto completo: {len(texto_archivo)} caracteres")
            print(f"[DEBUG] Longitud del texto enviado al LLM: {len(texto_limitado)} caracteres")
            print(f"[DEBUG] Primeros 500 caracteres del texto:")
            print(f"{texto_limitado[:500]}")
            print(f"[DEBUG] ======================================================")
            
            prompt = f"""Eres un asistente experto en extraer información estructurada de documentos oficiales y comunicados.

TEXTO DEL DOCUMENTO:
{texto_limitado}

INSTRUCCIONES:
1. Busca la FECHA en el encabezado del documento (primeras 20-30 líneas). La fecha puede estar en formato DD/MM/YYYY, DD-MM-YYYY, DD de MES de YYYY, o similar.
2. Busca el ASUNTO del comunicado. El asunto generalmente aparece después de palabras clave como "ASUNTO:", "REFERENCIA:", "TEMA:", o en una línea destacada del encabezado.
3. Si encuentras la fecha, conviértela al formato DD/MM/YYYY.
4. Si encuentras el asunto, extrae el texto completo del asunto.
5. Si no encuentras la fecha o el asunto, retorna null para ese campo.

IMPORTANTE:
- La fecha debe estar en el ENCABEZADO del documento (primeras líneas, antes del cuerpo del texto)
- El asunto debe ser el tema principal del comunicado, generalmente en mayúsculas o destacado
- Retorna SOLO un JSON válido con esta estructura exacta (sin comillas adicionales ni markdown):
{{
    "fecha": "DD/MM/YYYY" o null,
    "asunto": "Texto del asunto completo" o null
}}

Retorna únicamente el JSON, sin explicaciones ni texto adicional."""

            print(f"[DEBUG] Enviando petición a OpenAI con modelo: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en extraer información estructurada de documentos oficiales. Siempre respondes ÚNICAMENTE con JSON válido, sin explicaciones, sin markdown, sin texto adicional."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,  # Aumentado para permitir asuntos más largos
                temperature=0.0  # Temperatura 0 para máxima precisión
            )
            
            respuesta_texto = response.choices[0].message.content.strip()
            
            print(f"[DEBUG] Respuesta completa del LLM:")
            print(f"{respuesta_texto}")
            print(f"[DEBUG] ======================================================")
            
            # Intentar parsear JSON de la respuesta
            import json
            import re
            
            # Limpiar la respuesta (puede tener markdown o texto adicional)
            respuesta_limpia = respuesta_texto.strip()
            
            # Remover markdown code blocks
            if respuesta_limpia.startswith("```json"):
                respuesta_limpia = respuesta_limpia[7:]
            elif respuesta_limpia.startswith("```"):
                respuesta_limpia = respuesta_limpia[3:]
            if respuesta_limpia.endswith("```"):
                respuesta_limpia = respuesta_limpia[:-3]
            respuesta_limpia = respuesta_limpia.strip()
            
            # Buscar JSON en la respuesta usando un regex más robusto
            # Buscar desde la primera { hasta la última }
            json_match = re.search(r'\{.*\}', respuesta_limpia, re.DOTALL)
            if json_match:
                respuesta_limpia = json_match.group(0)
            
            print(f"[DEBUG] JSON extraído: {respuesta_limpia}")
            
            resultado = json.loads(respuesta_limpia)
            
            fecha = resultado.get("fecha")
            asunto = resultado.get("asunto")
            
            print(f"[DEBUG] Fecha extraída: {fecha}")
            print(f"[DEBUG] Asunto extraído: {asunto[:100] if asunto else None}...")
            
            return {
                "fecha": fecha,
                "asunto": asunto
            }
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Error al parsear JSON de LLM para fecha/asunto: {e}")
            print(f"[ERROR] Respuesta completa recibida: {respuesta_texto}")
            print(f"[ERROR] JSON intentado: {respuesta_limpia if 'respuesta_limpia' in locals() else 'N/A'}")
            import traceback
            traceback.print_exc()
            return {"fecha": None, "asunto": None}
        except Exception as e:
            print(f"[ERROR] Error al extraer fecha/asunto con LLM: {e}")
            print(f"[ERROR] Respuesta recibida: {respuesta_texto if 'respuesta_texto' in locals() else 'N/A'}")
            import traceback
            traceback.print_exc()
            return {"fecha": None, "asunto": None}
    
    def _generar_observacion_fallback(self, obligacion: str, cumplio: str) -> str:
        """
        Genera observación genérica cuando no hay LLM disponible
        
        Args:
            obligacion: Texto de la obligación
            cumplio: Estado de cumplimiento
            
        Returns:
            Observación genérica
        """
        if cumplio == "Cumplió":
            # Extraer palabras clave de la obligación
            if "Constitución" in obligacion or "Ley" in obligacion:
                return "La EMPRESA DE TELECOMUNICACIONES DE BOGOTÁ S.A. E.S.P acata la Constitución, la Ley, las normas legales y procedimientos establecidos por el Gobierno Nacional y Distrital, y demás disposiciones pertinentes."
            elif "especificaciones" in obligacion.lower() or "propuesta" in obligacion.lower():
                return "Se da cumplimiento con el presente informe y sus anexos."
            elif "Seguridad Social" in obligacion or "salud" in obligacion.lower():
                return "Se acredita el cumplimiento del Sistema de Seguridad Social, incluyendo salud, pensión, aportes parafiscales y riesgos laborales, mediante la presentación de las planillas de pago correspondientes y los certificados respectivos."
            else:
                return f"Se da cumplimiento a la obligación: {obligacion[:100]}..."
        else:
            return f"No se cumplió la obligación: {obligacion[:100]}..."
    
    def procesar_obligacion(self, obligacion: Dict, informes_aprobados_contexto: Optional[List[str]] = None, anio: Optional[int] = None, mes: Optional[int] = None) -> Dict:
        """
        Procesa una obligación y genera observación dinámica desde los anexos
        
        Args:
            obligacion: Diccionario con obligación. Puede tener:
                       - Formato nuevo: 'anexos': [{"ruta": "...", "revisar": bool, "nota": "..."}, ...]
                       - Formato antiguo (compatibilidad): 'anexo': "ruta", 'revisaranexo': bool
                       - 'defaultobservaciones': str - Observación por defecto si no se revisan anexos
            informes_aprobados_contexto: Lista de textos extraídos de los últimos 3 informes aprobados (opcional)
            
        Returns:
            Obligación con observación actualizada
        """
        # Si ya tiene observación y no queremos regenerarla, retornar tal cual
        if obligacion.get("observaciones") and not obligacion.get("regenerar_observacion", False):
            return obligacion
        
        # Obtener anexos (formato requerido)
        anexos = obligacion.get("anexos", [])
        
        # Si no hay anexos, la obligación no tiene anexos para procesar
        if not anexos or len(anexos) == 0:
            default_observaciones = obligacion.get("defaultobservaciones", "")
            if default_observaciones:
                print(f"[INFO] Obligación {obligacion.get('item', 'N/A')}: No hay anexos, usando observación por defecto")
                obligacion_actualizada = obligacion.copy()
                obligacion_actualizada["observaciones"] = default_observaciones
                obligacion_actualizada["observacion_generada_llm"] = False
                return obligacion_actualizada
        
        # Verificar si hay anexos que se deben revisar
        anexos_a_revisar = [anexo for anexo in anexos if anexo.get("revisar", True)]
        anexos_no_revisar = [anexo for anexo in anexos if not anexo.get("revisar", True)]
        
        # REGLA DE NEGOCIO: Si todos los anexos tienen revisar = false, usar defaultobservaciones directamente sin LLM
        if not anexos_a_revisar:
            default_observaciones = obligacion.get("defaultobservaciones", "")
            if default_observaciones:
                print(f"[INFO] Obligación {obligacion.get('item', 'N/A')}: REGLA DE NEGOCIO - Todos los anexos tienen revisar=false, usando observación por defecto (sin LLM)")
                obligacion_actualizada = obligacion.copy()
                obligacion_actualizada["observaciones"] = default_observaciones
                obligacion_actualizada["observacion_generada_llm"] = False
                return obligacion_actualizada
            else:
                print(f"[WARNING] Obligación {obligacion.get('item', 'N/A')}: Todos los anexos tienen revisar=false pero no hay defaultobservaciones, usando fallback")
        
        # Pre-descargar anexos que no se revisan pero que otros items podrían necesitar
        for anexo in anexos_no_revisar:
            ruta_anexo = anexo.get("ruta", "")
            if ruta_anexo and ruta_anexo != "-" and ruta_anexo.lower() != "no aplica":
                ruta_cache_key = ruta_anexo.strip().lower()
                if ruta_cache_key and ruta_cache_key not in self.cache_archivos_descargados:
                    print(f"[INFO] Pre-descargando archivo al cache para reutilización: {ruta_anexo}")
                    try:
                        ruta_completa_temp = self._resolver_ruta_anexo(ruta_anexo, anio=anio, mes=mes)
                        if ruta_completa_temp and isinstance(ruta_completa_temp, str):
                            if self.sharepoint_extractor.es_url_sharepoint(ruta_completa_temp) or ruta_completa_temp.startswith('/sites/') or ruta_completa_temp.startswith('/teams/'):
                                archivo_temp = self.sharepoint_extractor.descargar_archivo(ruta_completa_temp)
                                if archivo_temp and archivo_temp.exists():
                                    self.cache_archivos_descargados[ruta_cache_key] = archivo_temp
                                    self.archivos_temporales.append(archivo_temp)
                                    print(f"[INFO] Archivo pre-descargado y guardado en cache")
                    except Exception as e:
                        print(f"[DEBUG] No se pudo pre-descargar archivo (no crítico): {e}")
        
        # Procesar anexos que se deben revisar
        textos_anexos = []
        anexos_no_encontrados = []
        
        for anexo in anexos_a_revisar:
            ruta_anexo = anexo.get("ruta", "")
            nota_anexo = anexo.get("nota", "")
            
            if not ruta_anexo or ruta_anexo == "-" or ruta_anexo.lower() == "no aplica":
                continue
            
            print(f"[INFO] Procesando anexo {len(textos_anexos) + 1}/{len(anexos_a_revisar)} para obligación {obligacion.get('item', 'N/A')}: {ruta_anexo}")
            
            # Verificar si la ruta termina con % (búsqueda por prefijo)
            buscar_por_prefijo = ruta_anexo.strip().endswith('%')
            prefijo_busqueda = None
            ruta_para_resolver = ruta_anexo  # Ruta que se usará para resolver (sin % si lo tiene)
            
            if buscar_por_prefijo:
                # Extraer el prefijo (todo hasta el %)
                prefijo_busqueda = ruta_anexo.strip()[:-1].strip()  # Remover el % y espacios
                ruta_para_resolver = prefijo_busqueda  # Usar el prefijo sin % para la búsqueda
                print(f"[INFO] Búsqueda por prefijo detectada. Prefijo: {prefijo_busqueda}")
            else:
                print(f"[INFO] Búsqueda por nombre completo. Ruta: {ruta_anexo}")
            
            # Resolver ruta del anexo
            # Si es búsqueda por prefijo, pasar el prefijo sin %
            # Si es búsqueda por nombre completo, pasar la ruta completa
            ruta_completa = self._resolver_ruta_anexo(ruta_para_resolver, anio=anio, mes=mes, buscar_por_prefijo=buscar_por_prefijo, prefijo=prefijo_busqueda)
            if not ruta_completa:
                print(f"[WARNING] No se pudo resolver ruta del anexo: {ruta_anexo}")
                anexos_no_encontrados.append(ruta_anexo)
                continue
            
            print(f"[INFO] Ruta resuelta: {ruta_completa}")
            
            # Verificar existencia y descargar si es necesario
            archivo_existe = False
            archivo_temp_descargado = None
            ruta_cache_key = ruta_anexo.strip().lower()
            
            # Verificar cache primero
            if ruta_cache_key in self.cache_archivos_descargados:
                archivo_cache = self.cache_archivos_descargados[ruta_cache_key]
                if archivo_cache.exists():
                    print(f"[INFO] Archivo encontrado en cache, reutilizando: {ruta_anexo}")
                    archivo_existe = True
                    archivo_temp_descargado = archivo_cache
                    ruta_completa = str(archivo_temp_descargado)
                else:
                    del self.cache_archivos_descargados[ruta_cache_key]
            
            # Si no está en cache, intentar descargar
            if not archivo_existe and isinstance(ruta_completa, str):
                if self.sharepoint_extractor.es_url_sharepoint(ruta_completa) or ruta_completa.startswith('/sites/') or ruta_completa.startswith('/teams/'):
                    print(f"[INFO] Intentando descargar archivo desde SharePoint...")
                    try:
                        archivo_temp_descargado = self.sharepoint_extractor.descargar_archivo(ruta_completa)
                        if archivo_temp_descargado and archivo_temp_descargado.exists():
                            archivo_existe = True
                            self.cache_archivos_descargados[ruta_cache_key] = archivo_temp_descargado
                            self.archivos_temporales.append(archivo_temp_descargado)
                            ruta_completa = str(archivo_temp_descargado)
                            print(f"[INFO] Archivo descargado exitosamente y guardado en cache: {ruta_anexo}")
                        else:
                            print(f"[WARNING] No se pudo descargar el archivo desde SharePoint: {ruta_anexo}")
                            anexos_no_encontrados.append(ruta_anexo)
                    except Exception as e:
                        print(f"[WARNING] Error al descargar archivo desde SharePoint: {e}")
                        anexos_no_encontrados.append(ruta_anexo)
                else:
                    # Archivo local
                    ruta_path = Path(ruta_completa)
                    archivo_existe = ruta_path.exists()
                    if not archivo_existe:
                        print(f"[WARNING] El archivo no existe localmente: {ruta_completa}")
                        anexos_no_encontrados.append(ruta_anexo)
            
            # Extraer texto si el archivo existe
            if archivo_existe:
                print(f"[INFO] Archivo encontrado, extrayendo texto del anexo...")
                texto_anexo_actual = self.extraer_texto_archivo(ruta_completa)
                print(f"[INFO] Texto extraído: {len(texto_anexo_actual)} caracteres")
                
                # Agregar nota del anexo si existe
                if nota_anexo:
                    texto_anexo_actual = f"NOTA DEL ANEXO: {nota_anexo}\n\n{texto_anexo_actual}"
                
                textos_anexos.append(texto_anexo_actual)
            else:
                print(f"[WARNING] No se pudo procesar el anexo: {ruta_anexo}")
        
        # Si hay anexos no encontrados y se deben revisar, generar observación indicando que no existen
        if anexos_no_encontrados and anexos_a_revisar:
            mensaje_anexos_no_encontrados = f"Los siguientes archivos de anexo no existen: {', '.join(anexos_no_encontrados)}"
            print(f"[INFO] Generando observación indicando que los archivos no existen")
            obligacion_actualizada = obligacion.copy()
            obligacion_actualizada["observaciones"] = mensaje_anexos_no_encontrados
            obligacion_actualizada["observacion_generada_llm"] = False
            return obligacion_actualizada
        
        # Si no hay textos de anexos pero hay anexos a revisar, usar observación por defecto
        if not textos_anexos and anexos_a_revisar:
            default_observaciones = obligacion.get("defaultobservaciones", "")
            if default_observaciones:
                print(f"[INFO] No se pudo extraer texto de los anexos, usando observación por defecto")
                obligacion_actualizada = obligacion.copy()
                obligacion_actualizada["observaciones"] = default_observaciones
                obligacion_actualizada["observacion_generada_llm"] = False
                return obligacion_actualizada
        
        # Combinar textos de todos los anexos
        texto_anexo_combinado = "\n\n--- SEPARADOR ENTRE ANEXOS ---\n\n".join(textos_anexos)
        
        # Generar observación con el texto combinado de todos los anexos
        print(f"[INFO] Generando observación con LLM (cliente disponible: {bool(self.client)}, texto disponible: {len(texto_anexo_combinado) > 50})")
        observacion = self.generar_observacion_llm(
            texto_anexo=texto_anexo_combinado,
            obligacion=obligacion.get("obligacion", ""),
            periodicidad=obligacion.get("periodicidad", ""),
            cumplio=obligacion.get("cumplio", "Cumplió"),
            informes_aprobados_contexto=informes_aprobados_contexto
        )
        
        # Actualizar obligación con observación generada
        obligacion_actualizada = obligacion.copy()
        obligacion_actualizada["observaciones"] = observacion
        # Marcar si se generó con LLM
        observacion_fallback = self._generar_observacion_fallback(
            obligacion.get("obligacion", ""),
            obligacion.get("cumplio", "Cumplió")
        )
        generada_con_llm = bool(
            texto_anexo_combinado and 
            len(texto_anexo_combinado.strip()) > 50 and
            self.client and 
            observacion != observacion_fallback
        )
        obligacion_actualizada["observacion_generada_llm"] = generada_con_llm
        
        return obligacion_actualizada
    
    def _resolver_ruta_anexo(self, ruta_relativa: str, anio: Optional[int] = None, mes: Optional[int] = None, 
                            buscar_por_prefijo: bool = False, prefijo: Optional[str] = None) -> Optional[str]:
        """
        Resuelve una ruta relativa de anexo a Path absoluto o URL de SharePoint
        
        Args:
            ruta_relativa: Ruta como aparece en el JSON (ej: "11. 01SEP - 30SEP / 01 OBLIGACIONES GENERALES/ ...")
                          o URL de SharePoint. Si termina con %, se buscará por prefijo.
            anio: Año del informe (opcional, para actualizar dinámicamente la carpeta)
            mes: Mes del informe (opcional, para actualizar dinámicamente la carpeta)
            buscar_por_prefijo: Si True, busca archivos que empiecen con el prefijo
            prefijo: Prefijo a buscar (sin el %)
            
        Returns:
            Path absoluto al archivo, URL de SharePoint, o None si no se encuentra
        """
        # Verificar si es URL de SharePoint
        if self.sharepoint_extractor.es_url_sharepoint(ruta_relativa):
            return ruta_relativa
        
        # Normalizar ruta (reemplazar espacios y caracteres especiales)
        ruta_normalizada = ruta_relativa.replace(" / ", "/").replace(" /", "/").replace("/ ", "/")
        
        # Si es búsqueda por prefijo, manejar de forma especial
        if buscar_por_prefijo and prefijo:
            return self._buscar_archivo_por_prefijo(prefijo, anio=anio, mes=mes)
        
        # Si se proporcionan anio y mes, actualizar dinámicamente la carpeta del periodo
        if anio and mes:
            # Obtener el nombre de carpeta dinámico según el mes y año
            nombre_carpeta_dinamico = config.get_nombre_carpeta_sharepoint(anio, mes)
            
            # Buscar y reemplazar cualquier patrón de carpeta antigua en la ruta
            # Patrones posibles: "11. 01SEP - 30SEP", "01SEP - 30SEP", etc.
            import re
            # Patrón para detectar carpetas de periodo (ej: "11. 01SEP - 30SEP" o "01SEP - 30SEP")
            patron_carpeta = r'\d+\.\s*\d{2}[A-Z]{3}\s*-\s*\d{2}[A-Z]{3}|\d{2}[A-Z]{3}\s*-\s*\d{2}[A-Z]{3}'
            
            if re.search(patron_carpeta, ruta_normalizada):
                # Reemplazar la carpeta antigua con la nueva dinámica
                ruta_normalizada = re.sub(patron_carpeta, nombre_carpeta_dinamico, ruta_normalizada)
                print(f"[DEBUG] Ruta actualizada dinámicamente: {ruta_relativa} -> {ruta_normalizada}")
        
        # Buscar en diferentes ubicaciones posibles
        ubicaciones_posibles = [
            config.OUTPUT_DIR / ruta_normalizada,
            config.DATA_DIR / "anexos" / ruta_normalizada,
            config.DATA_DIR / "fuentes" / ruta_normalizada,
            Path(ruta_normalizada),  # Ruta absoluta
        ]
        
        for ubicacion in ubicaciones_posibles:
            if ubicacion.exists():
                return str(ubicacion)
        
        # Intentar buscar solo el nombre del archivo
        nombre_archivo = Path(ruta_relativa).name
        for ubicacion_base in [config.OUTPUT_DIR, config.DATA_DIR / "anexos", config.DATA_DIR / "fuentes"]:
            for archivo in ubicacion_base.rglob(nombre_archivo):
                return str(archivo)
        
        # Intentar buscar en SharePoint si está configurado
        if self.sharepoint_extractor.site_url:
            # Si la ruta no es una URL completa, construir ruta relativa del servidor
            # Las rutas vienen como: "13. 01NOV - 30NOV / 01 OBLIGACIONES GENERALES/ archivo.pdf"
            # Necesitamos convertir a: "/sites/OPERACIONES/[base_path]/13. 01NOV - 30NOV/01 OBLIGACIONES GENERALES/archivo.pdf"
            
            # Extraer la ruta base del sitio (ej: /sites/OPERACIONES)
            from urllib.parse import urlparse
            sitio_parsed = urlparse(self.sharepoint_extractor.site_url)
            sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
            
            print(f"[DEBUG] Resolviendo ruta de SharePoint:")
            print(f"  - Ruta original: {ruta_relativa}")
            print(f"  - Ruta normalizada: {ruta_normalizada}")
            print(f"  - Site URL: {self.sharepoint_extractor.site_url}")
            print(f"  - Site path parts: {sitio_path_parts}")
            print(f"  - Base path: {self.sharepoint_extractor.base_path}")
            
            # Construir ruta relativa del servidor
            if sitio_path_parts:
                # Ejemplo: sitio_path_parts = ['sites', 'OPERACIONES']
                # base_path = "Documentos/PROYECTOS/Año 2024/..."
                # ruta_normalizada = "13. 01NOV - 30NOV/01 OBLIGACIONES GENERALES/archivo.pdf"
                
                path_parts = sitio_path_parts.copy()
                
                # Agregar base_path si está configurado
                if self.sharepoint_extractor.base_path:
                    base_path_clean = self.sharepoint_extractor.base_path.strip('/').strip()
                    if base_path_clean:
                        # Dividir base_path en partes y agregar cada una
                        base_path_parts = [p for p in base_path_clean.split('/') if p]
                        print(f"  - Base path parts: {base_path_parts}")
                        path_parts.extend(base_path_parts)
                
                # Agregar la ruta del archivo
                ruta_archivo_clean = ruta_normalizada.lstrip('/')
                server_relative_url = '/' + '/'.join(path_parts) + '/' + ruta_archivo_clean
                print(f"[INFO] Intentando buscar en SharePoint con ruta relativa: {server_relative_url}")
                # Retornar la ruta relativa para que SharePoint la use directamente
                return server_relative_url
            else:
                # Fallback: construir URL completa
                ruta_sharepoint = ruta_normalizada.lstrip("/")
                url_sharepoint = f"{self.sharepoint_extractor.site_url.rstrip('/')}/{ruta_sharepoint}"
                print(f"[INFO] Intentando buscar en SharePoint: {url_sharepoint}")
                return url_sharepoint
        
        print(f"[WARNING] No se encontró archivo de anexo: {ruta_relativa}")
        return None
    
    def _buscar_archivo_por_prefijo(self, prefijo: str, anio: Optional[int] = None, mes: Optional[int] = None) -> Optional[str]:
        """
        Busca un archivo en SharePoint por prefijo (cuando la ruta termina con %)
        
        Args:
            prefijo: Prefijo del nombre del archivo (sin el %)
            anio: Año del informe (opcional, para actualizar dinámicamente la carpeta)
            mes: Mes del informe (opcional, para actualizar dinámicamente la carpeta)
            
        Returns:
            Ruta completa al archivo encontrado o None
        """
        print(f"[INFO] Buscando archivo por prefijo: {prefijo}")
        
        # Normalizar prefijo
        prefijo_normalizado = prefijo.replace(" / ", "/").replace(" /", "/").replace("/ ", "/")
        
        # Si se proporcionan anio y mes, actualizar dinámicamente la carpeta del periodo
        if anio and mes:
            nombre_carpeta_dinamico = config.get_nombre_carpeta_sharepoint(anio, mes)
            import re
            patron_carpeta = r'\d+\.\s*\d{2}[A-Z]{3}\s*-\s*\d{2}[A-Z]{3}|\d{2}[A-Z]{3}\s*-\s*\d{2}[A-Z]{3}'
            if re.search(patron_carpeta, prefijo_normalizado):
                prefijo_normalizado = re.sub(patron_carpeta, nombre_carpeta_dinamico, prefijo_normalizado)
                print(f"[DEBUG] Prefijo actualizado dinámicamente: {prefijo} -> {prefijo_normalizado}")
        
        # Extraer la carpeta y el nombre del archivo
        # El prefijo puede ser: "13. 01NOV - 30NOV / OBLIGACIONES ESPECIFICAS/ OBLIGACIÓN 7 CORREO DE RADICACION.PDF"
        # O: "13. 01NOV - 30NOV / 02 OBLIGACIONES ESPECIFICAS/ OBLIGACIÓN 32 CAM-INV-M02-F01-STOCK Mínimo"
        # Necesitamos separar la carpeta del nombre del archivo
        # Estrategia: buscar el último "/" y asumir que todo después es el nombre del archivo
        partes = prefijo_normalizado.split('/')
        if len(partes) < 2:
            # Solo hay nombre de archivo, buscar en la raíz
            carpeta_busqueda = ""
            nombre_prefijo = prefijo_normalizado.strip()
        else:
            # La última parte es el nombre del archivo, el resto es la carpeta
            carpeta_busqueda = '/'.join(partes[:-1]).strip()
            nombre_prefijo = partes[-1].strip()
        
        # Si el nombre_prefijo contiene "OBLIGACIÓN" seguido de números, podría ser parte de la carpeta
        # Pero por ahora asumimos que la última parte después del "/" es el nombre del archivo
        # Si el usuario necesita que "OBLIGACIÓN 32" sea parte de la carpeta, debe incluirla antes del último "/"
        
        print(f"[DEBUG] Carpeta de búsqueda: {carpeta_busqueda}")
        print(f"[DEBUG] Prefijo del nombre: {nombre_prefijo}")
        
        # Si no hay SharePoint configurado, intentar búsqueda local
        if not self.sharepoint_extractor.site_url:
            # Buscar localmente
            for ubicacion_base in [config.OUTPUT_DIR, config.DATA_DIR / "anexos", config.DATA_DIR / "fuentes"]:
                if carpeta_busqueda:
                    carpeta_path = ubicacion_base / carpeta_busqueda
                else:
                    carpeta_path = ubicacion_base
                
                if carpeta_path.exists() and carpeta_path.is_dir():
                    # Buscar archivos que empiecen con el prefijo
                    for archivo in carpeta_path.iterdir():
                        if archivo.is_file() and archivo.name.startswith(nombre_prefijo):
                            print(f"[INFO] Archivo encontrado localmente por prefijo: {archivo}")
                            return str(archivo)
        
        # Buscar en SharePoint
        try:
            # Construir ruta de carpeta para SharePoint
            if self.sharepoint_extractor.site_url:
                # Construir ruta relativa del servidor
                from urllib.parse import urlparse
                sitio_parsed = urlparse(self.sharepoint_extractor.site_url)
                sitio_path_parts = [p for p in sitio_parsed.path.split('/') if p]
                
                path_parts = sitio_path_parts.copy()
                
                # Agregar base_path si está configurado
                if self.sharepoint_extractor.base_path:
                    base_path_clean = self.sharepoint_extractor.base_path.strip('/').strip()
                    if base_path_clean:
                        base_path_parts = [p for p in base_path_clean.split('/') if p]
                        path_parts.extend(base_path_parts)
                
                # Agregar la carpeta de búsqueda
                if carpeta_busqueda:
                    carpeta_clean = carpeta_busqueda.lstrip('/')
                    ruta_carpeta_sharepoint = '/' + '/'.join(path_parts) + '/' + carpeta_clean
                else:
                    ruta_carpeta_sharepoint = '/' + '/'.join(path_parts)
                
                print(f"[INFO] Listando archivos en carpeta SharePoint: {ruta_carpeta_sharepoint}")
                
                # Listar archivos en la carpeta
                archivos = self.sharepoint_extractor.listar_archivos_en_carpeta(carpeta_busqueda)
                
                # Buscar archivos que empiecen con el prefijo
                archivos_coincidentes = []
                for archivo_info in archivos:
                    nombre_archivo = archivo_info.get('nombre', '')
                    if nombre_archivo.startswith(nombre_prefijo):
                        archivos_coincidentes.append(archivo_info)
                        print(f"[INFO] Archivo encontrado por prefijo: {nombre_archivo}")
                
                if archivos_coincidentes:
                    # Usar el primer archivo encontrado (o el más reciente si hay varios)
                    # Ordenar por fecha de modificación (más reciente primero)
                    archivos_coincidentes.sort(key=lambda x: x.get('fecha_modificacion', ''), reverse=True)
                    archivo_seleccionado = archivos_coincidentes[0]
                    
                    # Construir ruta completa del archivo
                    ruta_archivo_sharepoint = archivo_seleccionado.get('ruta_sharepoint') or archivo_seleccionado.get('ruta_completa', '')
                    if ruta_archivo_sharepoint:
                        print(f"[INFO] Archivo seleccionado: {archivo_seleccionado.get('nombre')} - {ruta_archivo_sharepoint}")
                        return ruta_archivo_sharepoint
                else:
                    print(f"[WARNING] No se encontraron archivos que empiecen con el prefijo '{nombre_prefijo}' en la carpeta '{carpeta_busqueda}'")
            else:
                print(f"[WARNING] SharePoint no está configurado, no se puede buscar por prefijo")
        except Exception as e:
            print(f"[WARNING] Error al buscar archivo por prefijo en SharePoint: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def limpiar_archivos_temporales(self):
        """Limpia archivos temporales descargados de SharePoint"""
        # Limpiar archivos únicos (sin duplicados)
        archivos_unicos = set(self.archivos_temporales)
        for archivo in archivos_unicos:
            try:
                if archivo.exists():
                    archivo.unlink()
            except Exception as e:
                print(f"[WARNING] Error al eliminar archivo temporal {archivo}: {e}")
        self.archivos_temporales.clear()
        self.cache_archivos_descargados.clear()


# Singleton
_extractor_observaciones = None

def get_extractor_observaciones(api_key: Optional[str] = None, model: str = "gpt-4o-mini",
                                sharepoint_site_url: Optional[str] = None,
                                sharepoint_client_id: Optional[str] = None,
                                sharepoint_client_secret: Optional[str] = None,
                                sharepoint_base_path: Optional[str] = None) -> ExtractorObservaciones:
    """Obtiene instancia singleton del extractor de observaciones"""
    global _extractor_observaciones
    if _extractor_observaciones is None:
        _extractor_observaciones = ExtractorObservaciones(
            api_key=api_key,
            model=model,
            sharepoint_site_url=sharepoint_site_url,
            sharepoint_client_id=sharepoint_client_id,
            sharepoint_client_secret=sharepoint_client_secret,
            sharepoint_base_path=sharepoint_base_path
        )
    return _extractor_observaciones

