"""
Servicio de conexión a MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

import config

logger = logging.getLogger(__name__)


class Database:
    """Clase para manejar la conexión a MongoDB"""
    
    client: Optional[AsyncIOMotorClient] = None
    database = None


db = Database()


async def connect_to_mongo():
    """Conecta a MongoDB con autenticación si está configurada"""
    mongodb_uri = config.MONGODB_URI
    db_name = config.MONGODB_DB_NAME
    
    try:
        # Construir URI con autenticación si hay usuario y contraseña
        if config.MONGODB_USER and config.MONGODB_PASSWORD:
            # Si ya viene una URI completa en MONGODB_URI, usarla
            if not mongodb_uri.startswith("mongodb://") or "@" in mongodb_uri:
                # Ya tiene autenticación o es una URI completa
                pass
            else:
                # Construir URI con autenticación
                mongodb_uri = f"mongodb://{config.MONGODB_USER}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}:{config.MONGODB_PORT}/{db_name}?authSource={config.MONGODB_AUTH_SOURCE}"
        
        db.client = AsyncIOMotorClient(mongodb_uri)
        db.database = db.client[db_name]
        
        # Ocultar contraseña en logs
        uri_log = mongodb_uri
        if config.MONGODB_PASSWORD:
            uri_log = mongodb_uri.replace(config.MONGODB_PASSWORD, "***")
        
        logger.info(f"Conectado a MongoDB: {db_name}")
        logger.debug(f"MongoDB URI: {uri_log}")
        
        # Verificar conexión
        await db.client.admin.command('ping')
        logger.info("Conexión a MongoDB verificada exitosamente")
        
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """Cierra la conexión a MongoDB"""
    if db.client:
        db.client.close()
        logger.info("Conexión a MongoDB cerrada")


def get_database():
    """Obtiene la instancia de la base de datos"""
    return db.database



