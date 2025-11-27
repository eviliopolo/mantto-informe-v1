from typing import Dict, Any
from fastapi import HTTPException, status
import logging
from ..services.section2_service import Section2Service
from ..generadores.seccion_2_mesa_servicio import GeneradorSeccion2

logger = logging.getLogger(__name__)


class Section2Controller:
    
    def __init__(self):
        self.service = Section2Service()
        self.generador = GeneradorSeccion2()

    async def get_section_by_index(
        self, 
        data: Dict[str, Any],         
    ) -> Dict[str, Any]:
        try:
            return await self.service.get_section_by_index(data)
        except Exception as e:
            logger.error(f"Error en controlador al obtener sección: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la sección: {str(e)}"
            )
    
    async def get_all_section(
        self, 
        data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            return await self.service.get_all_section(data)
        except Exception as e:
            logger.error(f"Error en controlador al obtener toda la sección: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la sección completa: {str(e)}"
            )
    
    async def send_data_section(
        self, 
        data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            
            """ EVALUAMOS A QUE SECCION SE REQUIERE ACTUALIZAR """
            id_section = data.get("section_id")
            

            return await self.service.send_data_section(data)
        except Exception as e:
            logger.error(f"Error en controlador al guardar datos: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al guardar los datos: {str(e)}"
            )

