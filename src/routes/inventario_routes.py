"""
Rutas para la gestión de inventario (Sección 4)
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, Query, Body, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..controllers.inventario_controller import InventarioController
from ..middleware.auth_middleware import auth_middleware
from ..services.database import get_database

router = APIRouter(prefix="/inventario", tags=["Inventario - Sección 4"])

inventario_controller = InventarioController()


# Helper para combinar texto y ruta (igual que Node.js)
def combinar_texto_y_ruta(subseccion: Dict[str, Any]) -> str:
    """Combina texto y ruta en un solo string separado por \\n"""
    if not subseccion:
        return ''
    
    texto = subseccion.get('texto', '')
    ruta = subseccion.get('ruta', '')
    
    if not texto and not ruta:
        return ''
    if not ruta:
        return texto
    if not texto:
        return ruta
    
    return f"{texto}\n{ruta}"


# Helper para separar texto y ruta (igual que Node.js)
def separar_texto_y_ruta(texto_combinado: str) -> Dict[str, str]:
    """Separa un string combinado en texto y ruta"""
    if not texto_combinado or not isinstance(texto_combinado, str):
        return {'texto': '', 'ruta': ''}
    
    lineas = texto_combinado.split('\n')
    
    if len(lineas) == 0:
        return {'texto': '', 'ruta': ''}
    
    if len(lineas) == 1:
        # Si solo hay una línea, asumimos que es texto
        return {'texto': lineas[0], 'ruta': ''}
    
    # Primera línea = texto, resto = ruta (unidas)
    texto = lineas[0]
    ruta = '\n'.join(lineas[1:])
    
    return {'texto': texto, 'ruta': ruta}


@router.get("", status_code=status.HTTP_200_OK)
async def get_inventario(
    anio: int = Query(..., description="Año del inventario"),
    mes: int = Query(..., description="Mes del inventario (1-12)"),
    seccion: str = Query("4", description="Sección del inventario"),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene el inventario para un año y mes específicos
    
    - **anio**: Año del inventario
    - **mes**: Mes del inventario (1-12)
    - **seccion**: Sección del inventario (por defecto "4")
    
    Requiere autenticación mediante Bearer token.
    """
    return await inventario_controller.get_inventario(anio, mes, seccion, db)


@router.put("/subseccion", status_code=status.HTTP_200_OK)
async def update_subseccion(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza una subsección del inventario
    
    Body esperado:
    {
        "anio": 2025,
        "mes": 11,
        "seccion": "4",
        "subseccion": "4.1",
        "datos": {
            "texto": "...",
            "ruta": "..."
        }
    }
    
    Requiere autenticación mediante Bearer token.
    """
    anio = data.get("anio")
    mes = data.get("mes")
    seccion = data.get("seccion", "4")
    subseccion = data.get("subseccion")
    datos = data.get("datos")
    
    if not anio or not mes or not subseccion or not datos:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio, mes, subseccion y datos son requeridos"
        )
    
    return await inventario_controller.update_subseccion(anio, mes, seccion, subseccion, datos, db)


@router.put("/subseccion/tabla", status_code=status.HTTP_200_OK)
async def update_tabla(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza una tabla específica de una subsección
    
    Body esperado:
    {
        "anio": 2025,
        "mes": 11,
        "seccion": "4",
        "subseccion": "4.2",
        "nombreTabla": "tablaEntradas",
        "datos": [
            {"item": "...", "cantidad": 0, "valor": "..."}
        ]
    }
    
    Requiere autenticación mediante Bearer token.
    """
    anio = data.get("anio")
    mes = data.get("mes")
    seccion = data.get("seccion", "4")
    subseccion = data.get("subseccion")
    nombre_tabla = data.get("nombreTabla")
    datos = data.get("datos")
    
    if not anio or not mes or not subseccion or not nombre_tabla or not isinstance(datos, list):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio, mes, subseccion, nombreTabla y datos (array) son requeridos"
        )
    
    return await inventario_controller.update_tabla(anio, mes, seccion, subseccion, nombre_tabla, datos, db)


# Endpoints específicos por subsección (compatibilidad con frontend)
@router.get("/4.1", status_code=status.HTTP_200_OK)
async def get_subseccion_41(
    anio: int = Query(..., description="Año del inventario"),
    mes: int = Query(..., description="Mes del inventario (1-12)"),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene la subsección 4.1 del inventario
    Compatible con el frontend existente (igual que Node.js)
    """
    inventario = await inventario_controller.get_inventario(anio, mes, "4", db)
    inventario_data = inventario.get("data", {})
    
    # La estructura puede ser subsecciones['4']['1'] o subsecciones['4.1']
    subsecciones = inventario_data.get("subsecciones", {})
    subseccion_41 = subsecciones.get('4', {}).get('1', {}) or subsecciones.get('4.1', {})
    
    # Combinar texto y ruta como en Node.js
    contenido_combinado = combinar_texto_y_ruta(subseccion_41)
    
    return {
        "anio": anio,
        "mes": mes,
        "seccion": "4",
        "contenido": contenido_combinado
    }


@router.put("/4.1", status_code=status.HTTP_200_OK)
async def update_subseccion_41(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza la subsección 4.1
    Compatible con el frontend existente (igual que Node.js)
    """
    anio = data.get("anio")
    mes = data.get("mes")
    contenido = data.get("contenido", "")
    
    if not anio or not mes or contenido is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio, mes y contenido son requeridos"
        )
    
    # Separar texto y ruta como en Node.js
    texto_ruta = separar_texto_y_ruta(contenido)
    
    return await inventario_controller.update_subseccion(
        anio, mes, "4", "4.1", texto_ruta, db
    )


@router.get("/4.2", status_code=status.HTTP_200_OK)
async def get_subseccion_42(
    anio: int = Query(..., description="Año del inventario"),
    mes: int = Query(..., description="Mes del inventario (1-12)"),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene la subsección 4.2 del inventario
    Compatible con el frontend existente (igual que Node.js)
    """
    inventario = await inventario_controller.get_inventario(anio, mes, "4", db)
    inventario_data = inventario.get("data", {})
    
    # La estructura puede ser subsecciones['4']['2'] o subsecciones['4.2']
    subsecciones = inventario_data.get("subsecciones", {})
    subseccion_42 = subsecciones.get('4', {}).get('2', {}) or subsecciones.get('4.2', {})
    
    return {
        "anio": anio,
        "mes": mes,
        "seccion": "4",
        "hayEntradas": subseccion_42.get("hayEntradas", False),
        "texto": subseccion_42.get("texto", ""),
        "comunicado": subseccion_42.get("comunicado", ""),
        "fechaIngreso": subseccion_42.get("fechaIngreso", ""),
        "tablaEntradas": subseccion_42.get("tablaEntradas", [])
    }


@router.put("/4.2", status_code=status.HTTP_200_OK)
async def update_subseccion_42(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza la subsección 4.2
    Compatible con el frontend existente (igual que Node.js)
    """
    anio = data.get("anio")
    mes = data.get("mes")
    hay_entradas = data.get("hayEntradas")
    
    if not anio or not mes or hay_entradas is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio, mes y hayEntradas son requeridos"
        )
    
    datos_subseccion = {
        "hayEntradas": hay_entradas,
        "texto": data.get("texto", ""),
        "comunicado": data.get("comunicado", ""),
        "fechaIngreso": data.get("fechaIngreso", ""),
        "tablaEntradas": data.get("tablaEntradas", []) if isinstance(data.get("tablaEntradas"), list) else []
    }
    
    return await inventario_controller.update_subseccion(
        anio, mes, "4", "4.2", datos_subseccion, db
    )


@router.get("/4.3", status_code=status.HTTP_200_OK)
async def get_subseccion_43(
    anio: int = Query(..., description="Año del inventario"),
    mes: int = Query(..., description="Mes del inventario (1-12)"),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene la subsección 4.3 del inventario
    Compatible con el frontend existente (igual que Node.js)
    """
    inventario = await inventario_controller.get_inventario(anio, mes, "4", db)
    inventario_data = inventario.get("data", {})
    
    # La estructura puede ser subsecciones['4']['3'] o subsecciones['4.3']
    subsecciones = inventario_data.get("subsecciones", {})
    subseccion_43 = subsecciones.get('4', {}).get('3', {}) or subsecciones.get('4.3', {})
    
    # tablaEquiposNoOperativos y tablaSiniestros son objetos, no arrays
    tabla_equipos_no_operativos = subseccion_43.get("tablaEquiposNoOperativos", {})
    if isinstance(tabla_equipos_no_operativos, list):
        # Si viene como array, convertir a objeto con estructura por defecto
        tabla_equipos_no_operativos = {"fecha": "", "comunicado": "", "estado": ""}
    elif not isinstance(tabla_equipos_no_operativos, dict):
        tabla_equipos_no_operativos = {"fecha": "", "comunicado": "", "estado": ""}
    
    tabla_siniestros = subseccion_43.get("tablaSiniestros", {})
    if isinstance(tabla_siniestros, list):
        # Si viene como array, convertir a objeto con estructura por defecto
        tabla_siniestros = {"fecha": "", "comunicado": "", "cantidad": ""}
    elif not isinstance(tabla_siniestros, dict):
        tabla_siniestros = {"fecha": "", "comunicado": "", "cantidad": ""}
    
    # Obtener nombre del mes para textoReintegro por defecto
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    nombre_mes = meses[mes - 1] if 1 <= mes <= 12 else 'Mes'
    texto_reintegro_default = f"Se radica los equipos al almacén SDSCJ que requieren reintegro por su no operatividad en el mes de {nombre_mes} del {anio}."
    
    return {
        "anio": anio,
        "mes": mes,
        "seccion": "4",
        "haySalidas": subseccion_43.get("haySalidas", False),
        "texto": subseccion_43.get("texto", ""),
        "tablaEquiposNoOperativos": tabla_equipos_no_operativos,
        "textoBajasNoOperativas": subseccion_43.get("textoBajasNoOperativas", ""),
        "tablaDetalleEquipos": subseccion_43.get("tablaDetalleEquipos", []),
        "haySiniestros": subseccion_43.get("haySiniestros", False),
        "textoSiniestros": subseccion_43.get("textoSiniestros", ""),
        "tablaSiniestros": tabla_siniestros,
        "textoReintegro": subseccion_43.get("textoReintegro", texto_reintegro_default),
        "tablaDetalleSiniestros": subseccion_43.get("tablaDetalleSiniestros", [])
    }


@router.put("/4.3", status_code=status.HTTP_200_OK)
async def update_subseccion_43(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza la subsección 4.3
    Compatible con el frontend existente (igual que Node.js)
    """
    anio = data.get("anio")
    mes = data.get("mes")
    hay_salidas = data.get("haySalidas")
    hay_siniestros = data.get("haySiniestros")
    
    if not anio or not mes or hay_salidas is None or hay_siniestros is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio, mes, haySalidas y haySiniestros son requeridos"
        )
    
    # tablaEquiposNoOperativos y tablaSiniestros deben ser objetos, no arrays
    tabla_equipos_no_operativos = data.get("tablaEquiposNoOperativos", {})
    if isinstance(tabla_equipos_no_operativos, list):
        tabla_equipos_no_operativos = {"fecha": "", "comunicado": "", "estado": ""}
    elif not isinstance(tabla_equipos_no_operativos, dict):
        tabla_equipos_no_operativos = {"fecha": "", "comunicado": "", "estado": ""}
    
    tabla_siniestros = data.get("tablaSiniestros", {})
    if isinstance(tabla_siniestros, list):
        tabla_siniestros = {"fecha": "", "comunicado": "", "cantidad": ""}
    elif not isinstance(tabla_siniestros, dict):
        tabla_siniestros = {"fecha": "", "comunicado": "", "cantidad": ""}
    
    datos_subseccion = {
        "haySalidas": hay_salidas,
        "texto": data.get("texto", ""),
        "tablaEquiposNoOperativos": tabla_equipos_no_operativos,
        "textoBajasNoOperativas": data.get("textoBajasNoOperativas", ""),
        "tablaDetalleEquipos": data.get("tablaDetalleEquipos", []) if isinstance(data.get("tablaDetalleEquipos"), list) else [],
        "haySiniestros": hay_siniestros,
        "textoSiniestros": data.get("textoSiniestros", ""),
        "tablaSiniestros": tabla_siniestros,
        "textoReintegro": data.get("textoReintegro", ""),
        "tablaDetalleSiniestros": data.get("tablaDetalleSiniestros", []) if isinstance(data.get("tablaDetalleSiniestros"), list) else []
    }
    
    return await inventario_controller.update_subseccion(
        anio, mes, "4", "4.3", datos_subseccion, db
    )


@router.get("/4.4", status_code=status.HTTP_200_OK)
async def get_subseccion_44(
    anio: int = Query(..., description="Año del inventario"),
    mes: int = Query(..., description="Mes del inventario (1-12)"),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtiene la subsección 4.4 del inventario
    Compatible con el frontend existente (igual que Node.js)
    """
    inventario = await inventario_controller.get_inventario(anio, mes, "4", db)
    inventario_data = inventario.get("data", {})
    
    # La estructura puede ser subsecciones['4']['4'] o subsecciones['4.4']
    subsecciones = inventario_data.get("subsecciones", {})
    subseccion_44 = subsecciones.get('4', {}).get('4', {}) or subsecciones.get('4.4', {})
    
    # tablaGestionInclusion es un objeto, no un array (igual que Node.js)
    tabla_gestion = subseccion_44.get("tablaGestionInclusion", {})
    if isinstance(tabla_gestion, list) and len(tabla_gestion) > 0:
        # Si viene como array, tomar el primer elemento
        tabla_gestion = tabla_gestion[0]
    elif not isinstance(tabla_gestion, dict):
        # Si no es dict ni array válido, usar estructura por defecto
        tabla_gestion = {
            "item": 1,
            "fecha": "",
            "consecutivoETB": "",
            "descripcion": ""
        }
    
    return {
        "anio": anio,
        "mes": mes,
        "seccion": "4",
        "texto": subseccion_44.get("texto", ""),
        "tablaGestionInclusion": tabla_gestion
    }


@router.put("/4.4", status_code=status.HTTP_200_OK)
async def update_subseccion_44(
    data: Dict[str, Any] = Body(...),
    token_payload: dict = Depends(auth_middleware),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Dict[str, Any]:
    """
    Actualiza la subsección 4.4
    Compatible con el frontend existente (igual que Node.js)
    """
    anio = data.get("anio")
    mes = data.get("mes")
    
    if not anio or not mes:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="anio y mes son requeridos"
        )
    
    # tablaGestionInclusion es un objeto (igual que Node.js)
    # Pero en MongoDB lo guardamos como tablaGestionInclusion (objeto), no como array
    tabla_gestion = data.get("tablaGestionInclusion", {})
    if not isinstance(tabla_gestion, dict):
        tabla_gestion = {
            "item": 1,
            "fecha": "",
            "consecutivoETB": "",
            "descripcion": ""
        }
    
    datos_subseccion = {
        "texto": data.get("texto", ""),
        "tablaGestionInclusion": tabla_gestion
    }
    
    return await inventario_controller.update_subseccion(
        anio, mes, "4", "4.4", datos_subseccion, db
    )

