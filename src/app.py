# """
# Aplicación principal FastAPI para el sistema de autenticación y roles
# """
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import config
from src.routes import auth_routes
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
    logger.info("Iniciando aplicación...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Cerrando aplicación...")
    await close_mongo_connection()


# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Autenticación y Roles - Mantto Informe",
    description="API para autenticación y control de acceso basado en roles",
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

# # Incluir rutas
app.include_router(auth_routes.router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Autenticación y Roles - Mantto Informe API",
        "version": "1.0.0",
        "docs": "/docs"
    }


