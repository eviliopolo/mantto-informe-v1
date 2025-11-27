from datetime import datetime
from typing import Dict, Any, Optional
from src.services.database import get_database


async def get_section2(anio: int, mes: int, user_id: int, name_file: str):
    db = get_database()
    collection = db["section2"]
    
    document = await collection.find_one({"anio": anio, "mes": mes})
    
    if not document:
        await build_section2(anio, mes, user_id, name_file)
        document = await collection.find_one({"anio": anio, "mes": mes})
    
    return document    




# ESTE ES EL ESQUEMA BASE DEL DOCUMENTO EN CASO QUE NO EXISTA #
async def build_section2(anio: int, mes: int , user_id: int, name_file: str):

    db = get_database()
    datetime_now = datetime.now()    
    collection = db["section2"]
    user_created = user_id    
    document = await collection.insert_one(
        { 
        "section": "2",
        "title": "INFORME DE MESA DE SERVICIO",
        "anio": anio, 
        "mes": mes,  
        "name_file": name_file,
        "level": 1,      
        "created_at": datetime_now,
        "updated_at": datetime_now,
        "user_created": user_created,
        "user_updated": user_created,
        "index": [
             {
                "id": "2",
                "level": 1,
                "title": "2. INFORME DE MESA DE SERVICIO",
                "content": {
                    "parrafo1": "",
                    "image": "",
                    "parrafo2": "",
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.1",
                "level": 2,
                "title": "2.1 INFORME DE MESA DE SERVICIO",
                "content": {
                    "documento_1": "",
                    "image": "",
                    "tabla_1": [
                        {"id": 0, "fecha" : "valor1", "referencia" : "valor2", "radicado" : "valor3"},                        
                    ]
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.2",
                "level": 2,
                "title": "HERRAMIENTAS DE TRABAJO",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,     
                "updated_at": datetime_now,
            },
            {
                "id": "2.3",
                "level": 2,
                "title": "VISITAS DE DIAGNÓSTICOS A SUBSISTEMAS",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.4",
                "level": 2,
                "title": "INFORME CONSOLIDADO DEL ESTADO DE LOS TICKETS ADMINISTRATIVOS",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5",
                "level": 2,
                "title": "ESCALAMIENTOS",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.1",
                "level": 3,
                "title": "ENEL",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.2",
                "level": 3,
                "title": "CAÍDA MASIVA",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.3",
                "level": 3,
                "title": "CONECTIVIDAD",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.6",
                "level": 2,
                "title": "INFORME ACTUALIZADO DE HOJAS DE VIDA DE LOS PUNTOS Y SUBSISTEMAS DE VIDEO VIGILANCIA",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.7",
                "level": 2,
                "title": "INFORME EJECUTIVO DEL ESTADO DEL SISTEMA",
                "content": "",
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            }
        ],
        }
    )
    return document