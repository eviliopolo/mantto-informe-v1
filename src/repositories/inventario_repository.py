"""
Repositorio para acceso a datos de inventario (Sección 4)
"""
from typing import Dict, Any, Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class InventarioRepository:
    """Repositorio para gestionar datos de inventario en MongoDB"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.inventarios
    
    async def get_inventario(self, anio: int, mes: int, seccion: str = "4") -> Optional[Dict[str, Any]]:
        """
        Obtiene el inventario para un año, mes y sección específicos
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario (por defecto "4")
            
        Returns:
            Dict con los datos del inventario o None si no existe
        """
        try:
            inventario = await self.collection.find_one({
                "anio": anio,
                "mes": mes,
                "seccion": seccion
            })
            
            if inventario:
                # Convertir ObjectId a string
                inventario["_id"] = str(inventario["_id"])
            
            return inventario
        except Exception as e:
            logger.error(f"Error al obtener inventario: {e}")
            raise
    
    async def create_inventario(self, inventario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo inventario
        
        Args:
            inventario_data: Datos del inventario a crear
            
        Returns:
            Dict con el inventario creado
        """
        try:
            result = await self.collection.insert_one(inventario_data)
            inventario_data["_id"] = str(result.inserted_id)
            return inventario_data
        except Exception as e:
            logger.error(f"Error al crear inventario: {e}")
            raise
    
    async def update_inventario(self, anio: int, mes: int, seccion: str, inventario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un inventario existente o lo crea si no existe
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario
            inventario_data: Datos a actualizar
            
        Returns:
            Dict con el inventario actualizado
        """
        try:
            # Preparar datos para actualización
            update_data = {
                "anio": anio,
                "mes": mes,
                "seccion": seccion,
                **inventario_data
            }
            
            result = await self.collection.find_one_and_update(
                {"anio": anio, "mes": mes, "seccion": seccion},
                {"$set": update_data},
                upsert=True,
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
            
            return result
        except Exception as e:
            logger.error(f"Error al actualizar inventario: {e}")
            raise
    
    async def update_subseccion(self, anio: int, mes: int, seccion: str, subseccion: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una subsección específica del inventario
        Usa la misma estructura que Node.js: subsecciones.4.1, subsecciones.4.2, etc.
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario
            subseccion: Nombre de la subsección (ej: "4.1", "4.2")
            datos: Datos de la subsección a actualizar
            
        Returns:
            Dict con el inventario actualizado
        """
        try:
            # Usar la misma estructura que Node.js: subsecciones.4.1, subsecciones.4.2, etc.
            # Esto permite compatibilidad con la estructura anidada subsecciones['4']['1']
            update_path = f"subsecciones.{subseccion}"
            
            result = await self.collection.find_one_and_update(
                {"anio": anio, "mes": mes, "seccion": seccion},
                {"$set": {update_path: datos}},
                upsert=True,
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
            
            return result
        except Exception as e:
            logger.error(f"Error al actualizar subsección: {e}")
            raise
    
    async def update_tabla(self, anio: int, mes: int, seccion: str, subseccion: str, nombre_tabla: str, datos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Actualiza una tabla específica de una subsección
        
        Args:
            anio: Año del inventario
            mes: Mes del inventario (1-12)
            seccion: Sección del inventario
            subseccion: Nombre de la subsección (ej: "4.1", "4.2")
            nombre_tabla: Nombre de la tabla (ej: "tablaEntradas", "tablaEquiposNoOperativos")
            datos: Lista de filas de la tabla
            
        Returns:
            Dict con el inventario actualizado
        """
        try:
            update_path = f"subsecciones.{subseccion}.{nombre_tabla}"
            result = await self.collection.find_one_and_update(
                {"anio": anio, "mes": mes, "seccion": seccion},
                {"$set": {update_path: datos}},
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
            
            return result
        except Exception as e:
            logger.error(f"Error al actualizar tabla: {e}")
            raise

