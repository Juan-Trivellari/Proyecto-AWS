"""
Rutas (endpoints) para la entidad Alumno.
"""

from fastapi import APIRouter, status, Query
from typing import List
from app.schemas.alumno_schema import AlumnoCreate, AlumnoUpdate, AlumnoResponse
from app.services import alumnos_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AlumnoResponse], status_code=status.HTTP_200_OK)
async def listar_alumnos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
):
    """Obtener lista de todos los alumnos."""
    try:
        alumnos = alumnos_service.obtener_todos_alumnos()
        return alumnos[skip : skip + limit]
    except Exception as e:
        logger.error(f"Error al listar alumnos: {str(e)}")
        raise


@router.get("/{alumno_id}", response_model=AlumnoResponse, status_code=status.HTTP_200_OK)
async def obtener_alumno(alumno_id: int):
    """Obtener un alumno por su ID."""
    return alumnos_service.obtener_alumno_por_id(alumno_id)


@router.post("", response_model=AlumnoResponse, status_code=status.HTTP_201_CREATED)
async def crear_alumno(alumno: AlumnoCreate):
    """Crear un nuevo alumno."""
    try:
        logger.info(f"Creando alumno con matrícula {alumno.matricula}")
        return alumnos_service.crear_alumno(alumno)
    except Exception as e:
        logger.error(f"Error al crear alumno: {str(e)}")
        raise


@router.put("/{alumno_id}", response_model=AlumnoResponse, status_code=status.HTTP_200_OK)
async def actualizar_alumno(alumno_id: int, alumno: AlumnoUpdate):
    """Actualizar un alumno existente."""
    try:
        logger.info(f"Actualizando alumno ID {alumno_id}")
        return alumnos_service.actualizar_alumno(alumno_id, alumno)
    except Exception as e:
        logger.error(f"Error al actualizar alumno: {str(e)}")
        raise


@router.delete("/{alumno_id}", status_code=status.HTTP_200_OK)
async def eliminar_alumno(alumno_id: int):
    """Eliminar un alumno."""
    try:
        logger.info(f"Eliminando alumno ID {alumno_id}")
        return alumnos_service.eliminar_alumno(alumno_id)
    except Exception as e:
        logger.error(f"Error al eliminar alumno: {str(e)}")
        raise


@router.get("/stats/resumen", status_code=status.HTTP_200_OK)
async def obtener_estadisticas_alumnos():
    """Obtener estadísticas de alumnos."""
    return alumnos_service.obtener_estadisticas()