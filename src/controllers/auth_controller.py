"""
Controlador de autenticación
"""
from typing import Dict, Any
from fastapi import HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId
import jwt
import bcrypt
from ..services.external_auth_service import ExternalAuthService
from ..services.role_mapping_service import RoleMappingService
from ..services.jwt_service import JWTService

from ..services.database import get_database
from ..models.user import User, UserResponse
import logging

logger = logging.getLogger(__name__)


class AuthController:
    """Controlador para manejar la autenticación"""
    
    def __init__(self):
        self.external_auth_service = ExternalAuthService()
        self.jwt_service = JWTService()
    
    async def login(self, credentials: Dict[str, str], db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Inicia sesión con email/username y contraseña
        Autentica directamente contra MongoDB sin depender de API externa
        
        Args:
            credentials: Dict con 'email' o 'username' y 'password'
            db: Instancia de la base de datos
            
        Returns:
            Dict con token JWT y datos del usuario
        """
        email = credentials.get("username")
        password = credentials.get("password")

        print(email, password)
        
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email/username y contraseña son requeridos"
            )
        
        try:
            users_collection = db.users
            
            # Buscar usuario por email o username
            user = await users_collection.find_one({
                "$or": [
                    {"email": email},
                    {"username": email}
                ]
            })
            
            # Si el usuario no existe, crear uno por defecto (solo para desarrollo)
            if not user:
                logger.info(f"Usuario no encontrado, creando usuario por defecto: {email}")
                # Hashear contraseña
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Crear usuario con rol por defecto
                new_user = {
                    "email": email,
                    "username": email.split("@")[0] if "@" in email else email,
                    "password": password_hash,
                    "access_role_name": "admin_info_general",  # Rol por defecto
                    "modules": ["info_general", "inventario"],  # Módulos por defecto
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": None
                }
                
                result = await users_collection.insert_one(new_user)
                new_user["_id"] = result.inserted_id
                user = new_user
            else:
                # Verificar contraseña
                stored_password = user.get("password")
                if not stored_password:
                    # Si no hay contraseña almacenada, crear una nueva (migración)
                    logger.info(f"Usuario sin contraseña, creando hash para: {email}")
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    await users_collection.update_one(
                        {"_id": user["_id"]},
                        {"$set": {"password": password_hash}}
                    )
                else:
                    # Verificar contraseña
                    if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        logger.warning(f"Contraseña incorrecta para usuario: {email}")
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales inválidas"
                        )
            
            # Verificar que el usuario esté activo
            if not user.get("is_active", True):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario inactivo"
                )
            
            # Obtener rol y módulos
            role_mapping_service = RoleMappingService(db)
            access_role_name = user.get("access_role_name") or "admin_info_general"
            modules = user.get("modules", [])
            
            # Si no tiene módulos, obtenerlos del rol
            if not modules:
                modules = await role_mapping_service.get_user_modules_from_role(access_role_name) or ["info_general", "inventario"]
            
            # Actualizar último login
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            # Generar token JWT local
            token_payload = {
                "sub": str(user["_id"]),
                "email": user.get("email", email),
                "username": user.get("username", email),
                "access_role_name": access_role_name,
                "modules": modules
            }
            token = self.jwt_service.generate_token(token_payload)
            
            # Preparar respuesta
            user_response = UserResponse(
                id=str(user["_id"]),
                email=user.get("email", email),
                username=user.get("username", email),
                access_role_name=access_role_name,
                modules=modules,
                is_active=user.get("is_active", True),
                last_login=datetime.utcnow()
            )
            
            logger.info(f"Login exitoso para usuario: {email}")
            return {
                "success": True,
                "message": "Login exitoso",
                "data": {
                    "token": token,
                    "user": user_response.model_dump()
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en login: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    async def verify_token(self, token_payload: Dict[str, Any], db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Verifica un token JWT y retorna información del usuario
        
        Args:
            token_payload: Payload del token JWT decodificado
            db: Instancia de la base de datos
            
        Returns:
            Dict con datos del usuario
        """
        user_id = token_payload.get("sub") or token_payload.get("user_id")
        email = token_payload.get("email")
        
        users_collection = db.users
        
        # Buscar por ID o email
        if user_id:
            user = await users_collection.find_one({"_id": ObjectId(user_id)})
        elif email:
            user = await users_collection.find_one({"email": email})
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no se pudo identificar al usuario"
            )
        
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        user_response = UserResponse(
            id=str(user["_id"]),
            email=user.get("email", ""),
            username=user.get("username", ""),
            access_role_name=user.get("access_role_name"),
            modules=user.get("modules", []),
            is_active=user.get("is_active", True),
            last_login=user.get("last_login")
        )
        
        return {
            "success": True,
            "data": user_response.model_dump()
        }
    
    async def get_profile(self, user_id: str, db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Obtiene el perfil completo del usuario
        
        Args:
            user_id: ID del usuario
            db: Instancia de la base de datos
            
        Returns:
            Dict con datos del perfil del usuario
        """
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario requerido"
            )
        
        users_collection = db.users
        
        try:
            user = await users_collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario inválido"
            )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        user_response = UserResponse(
            id=str(user["_id"]),
            email=user.get("email", ""),
            username=user.get("username", ""),
            access_role_name=user.get("access_role_name"),
            modules=user.get("modules", []),
            is_active=user.get("is_active", True),
            last_login=user.get("last_login")
        )
        
        return {
            "success": True,
            "data": user_response.model_dump()
        }
 

