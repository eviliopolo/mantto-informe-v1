"""
Aplicación principal FastAPI para el sistema de generación de informes
"""
import logging
import config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import routes
from src.services.database import connect_to_mongo, close_mongo_connection

# # Configurar logging
logging.basicConfig(
    level=logging.INFO if config.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup
    logger.info("=" * 80)
    logger.info("Iniciando aplicación FastAPI...")
    logger.info("=" * 80)
    
    # Conectar a MongoDB
    try:
        await connect_to_mongo()
        logger.info("✓ MongoDB conectado")
    except Exception as e:
        logger.warning(f"No se pudo conectar a MongoDB: {e}")
    
    yield
    
    # Shutdown
    logger.info("=" * 80)
    logger.info("Cerrando aplicación...")
    logger.info("=" * 80)
    
    # Cerrar conexión a MongoDB
    try:
        await close_mongo_connection()
        logger.info("✓ Conexión a MongoDB cerrada")
    except Exception as e:
        logger.warning(f"Error al cerrar conexión a MongoDB: {e}")


# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Generación de Informes Mensuales ETB",
    description="API para generar informes mensuales de mantenimiento con extracción dinámica de datos",
    version="1.0.0",
    lifespan=lifespan
)

# # Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Generación de Informes Mensuales ETB API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "obligaciones": "/api/obligaciones/procesar",
            "comunicados_emitidos": "/api/comunicados/emitidos",
            "comunicados_recibidos": "/api/comunicados/recibidos",
            "seccion1_generar": "/api/seccion1/generar",
            "seccion1_descargar": "/api/seccion1/descargar",
            "seccion4_generar": "/api/seccion4/generar",
            "seccion4_descargar": "/api/seccion4/descargar",
            "seccion5_procesar_excel": "/api/seccion5/procesar-excel",
            "seccion5_obtener_datos": "/api/seccion5/obtener-datos",
            "seccion5_generar": "/api/seccion5/generar",
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

    
try: 
    for route in routes:
        app.include_router(route, prefix="/api")
        logger.info(f"✓ Rutas de {route.tags[0]} incluidas")
except Exception as e:
    logger.warning(f"No se pudieron incluir rutas de {route.tags[0]}: {e}")

