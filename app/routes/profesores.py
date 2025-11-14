"""
Rutas (endpoints) para la entidad Profesor.
"""

from fastapi import APIRouter, status, Query
from typing import List
from app.schemas.profesor_schema import ProfesorCreate, ProfesorUpdate, ProfesorResponse
from app.services import profesores_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[ProfesorResponse], status_code=status.HTTP_200_OK)
async def listar_profesores(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
):
    """Obtener lista de todos los profesores."""
    try:
        profesores = profesores_service.obtener_todos_profesores()
        return profesores[skip : skip + limit]
    except Exception as e:
        logger.error(f"Error al listar profesores: {str(e)}")
        raise


@router.get("/{profesor_id}", response_model=ProfesorResponse, status_code=status.HTTP_200_OK)
async def obtener_profesor(profesor_id: int):
    """Obtener un profesor por su ID."""
    return profesores_service.obtener_profesor_por_id(profesor_id)


@router.post("", response_model=ProfesorResponse, status_code=status.HTTP_201_CREATED)
async def crear_profesor(profesor: ProfesorCreate):
    """Crear un nuevo profesor."""
    try:
        logger.info(f"Creando profesor con número {profesor.numeroEmpleado}")
        return profesores_service.crear_profesor(profesor)
    except Exception as e:
        logger.error(f"Error al crear profesor: {str(e)}")
        raise


@router.put("/{profesor_id}", response_model=ProfesorResponse, status_code=status.HTTP_200_OK)
async def actualizar_profesor(profesor_id: int, profesor: ProfesorUpdate):
    """Actualizar un profesor existente."""
    try:
        logger.info(f"Actualizando profesor ID {profesor_id}")
        return profesores_service.actualizar_profesor(profesor_id, profesor)
    except Exception as e:
        logger.error(f"Error al actualizar profesor: {str(e)}")
        raise


@router.delete("/{profesor_id}", status_code=status.HTTP_200_OK)
async def eliminar_profesor(profesor_id: int):
    """Eliminar un profesor."""
    try:
        logger.info(f"Eliminando profesor ID {profesor_id}")
        return profesores_service.eliminar_profesor(profesor_id)
    except Exception as e:
        logger.error(f"Error al eliminar profesor: {str(e)}")
        raise


@router.get("/stats/resumen", status_code=status.HTTP_200_OK)
async def obtener_estadisticas_profesores():
    """Obtener estadísticas de profesores."""
    return profesores_service.obtener_estadisticas()