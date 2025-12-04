"""
Controlador para la gestión de inventario (Sección 4)
"""
from typing import Dict, Any, Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from ..repositories.inventario_repository import InventarioRepository
import logging

logger = logging.getLogger(__name__)


class InventarioController:
    """Controlador para manejar operaciones de inventario"""
    
    def __init__(self):
        self.repository = None
    
    def _get_repository(self, db: AsyncIOMotorDatabase) -> InventarioRepository:
        """Obtiene o crea el repositorio"""
        if self.repository is None:
            self.repository = InventarioRepository(db)
        return self.repository
    
    async def get_inventario(
        self,
        anio: int,
        mes: int,
        seccion: str = "4",
        db: Optional[AsyncIOMotorDatabase] = None
    ) -> Dict[str, Any]:
        """
        Obtiene el inventario para un año y mes específicos
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario (por defecto "4")
            db: Instancia de la base de datos
            
        Returns:
            Dict con los datos del inventario
        """
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Base de datos no disponible"
            )
        
        try:
            repository = self._get_repository(db)
            inventario = await repository.get_inventario(anio, mes, seccion)
            
            # Si no existe, crear uno con estructura inicial (igual que Node.js)
            if not inventario:
                inventario_data = {
                    "anio": anio,
                    "mes": mes,
                    "seccion": seccion,
                    "subsecciones": {
                        "4.1": {
                            "texto": "Se relaciona el inventario del sistema de videovigilancia de Bogotá, durante el desarrollo del contrato, donde registran los componentes de cada punto de videovigilancia.\n\nSe relaciona en la ruta {{root_mes}}\\01 OBLIGACIONES GENERALES\\OBLIGACIÓN 2,5,6,9,13\\ANEXO BIENES Y SERVICIOS\\INVENTARIO.xlsx",
                            "ruta": ""
                        },
                        "4.2": {
                            "hayEntradas": False,
                            "texto": "",
                            "comunicado": "",
                            "fechaIngreso": "",
                            "tablaEntradas": []
                        },
                        "4.3": {
                            "haySalidas": False,
                            "texto": "",
                            "tablaEquiposNoOperativos": {"fecha": "", "comunicado": "", "estado": ""},
                            "textoBajasNoOperativas": "",
                            "tablaDetalleEquipos": [],
                            "haySiniestros": False,
                            "textoSiniestros": "",
                            "tablaSiniestros": {"fecha": "", "comunicado": "", "cantidad": ""},
                            "textoReintegro": "",
                            "tablaDetalleSiniestros": []
                        },
                        "4.4": {
                            "texto": "",
                            "tablaGestionInclusion": {
                                "item": 1,
                                "fecha": "",
                                "consecutivoETB": "",
                                "descripcion": ""
                            }
                        }
                    }
                }
                inventario = await repository.create_inventario(inventario_data)
            
            return {
                "success": True,
                "data": inventario
            }
        except Exception as e:
            logger.error(f"Error al obtener inventario: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener inventario: {str(e)}"
            )
    
    async def update_subseccion(
        self,
        anio: int,
        mes: int,
        seccion: str,
        subseccion: str,
        datos: Dict[str, Any],
        db: Optional[AsyncIOMotorDatabase] = None
    ) -> Dict[str, Any]:
        """
        Actualiza una subsección del inventario
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario
            subseccion: Nombre de la subsección (ej: "4.1", "4.2")
            datos: Datos de la subsección a actualizar
            db: Instancia de la base de datos
            
        Returns:
            Dict con el inventario actualizado
        """
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Base de datos no disponible"
            )
        
        try:
            repository = self._get_repository(db)
            inventario = await repository.update_subseccion(anio, mes, seccion, subseccion, datos)
            
            return {
                "success": True,
                "data": inventario
            }
        except Exception as e:
            logger.error(f"Error al actualizar subsección: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar subsección: {str(e)}"
            )
    
    async def update_tabla(
        self,
        anio: int,
        mes: int,
        seccion: str,
        subseccion: str,
        nombre_tabla: str,
        datos: List[Dict[str, Any]],
        db: Optional[AsyncIOMotorDatabase] = None
    ) -> Dict[str, Any]:
        """
        Actualiza una tabla específica de una subsección
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario
            subseccion: Nombre de la subsección (ej: "4.1", "4.2")
            nombre_tabla: Nombre de la tabla (ej: "tablaEntradas")
            datos: Lista de filas de la tabla
            db: Instancia de la base de datos
            
        Returns:
            Dict con el inventario actualizado
        """
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Base de datos no disponible"
            )
        
        try:
            repository = self._get_repository(db)
            inventario = await repository.update_tabla(anio, mes, seccion, subseccion, nombre_tabla, datos)
            
            return {
                "success": True,
                "data": inventario
            }
        except Exception as e:
            logger.error(f"Error al actualizar tabla: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar tabla: {str(e)}"
            )

