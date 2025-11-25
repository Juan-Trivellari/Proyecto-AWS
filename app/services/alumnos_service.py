"""
Servicio CRUD para Alumnos - AJUSTADO PARA TESTS
"""

from typing import Optional, List, Dict, Any
from app.schemas.alumno_schema import AlumnoCreate, AlumnoUpdate, AlumnoResponse
from app.utils.exceptions import ValidationError, NotFoundError
import logging

logger = logging.getLogger(__name__)

alumnos_db: List[Dict[str, Any]] = []
_next_alumno_id: int = 1


def _obtener_siguiente_id() -> int:
    global _next_alumno_id
    id_actual = _next_alumno_id
    _next_alumno_id += 1
    return id_actual


def _matricula_existe(matricula: str, excluir_id: Optional[int] = None) -> bool:
    for alumno in alumnos_db:
        if alumno["matricula"] == matricula:
            if excluir_id is None or alumno["id"] != excluir_id:
                return True
    return False


def _id_existe(id: int) -> bool:
    for alumno in alumnos_db:
        if alumno["id"] == id:
            return True
    return False


def obtener_todos_alumnos() -> List[AlumnoResponse]:
    logger.info(f"Obteniendo {len(alumnos_db)} alumnos")
    return [AlumnoResponse(**alumno) for alumno in alumnos_db]


def obtener_alumno_por_id(alumno_id: int) -> AlumnoResponse:
    for alumno in alumnos_db:
        if alumno["id"] == alumno_id:
            logger.info(f"Alumno encontrado: ID {alumno_id}")
            return AlumnoResponse(**alumno)
    
    logger.warning(f"Alumno no encontrado: ID {alumno_id}")
    raise NotFoundError(
        f"Alumno con ID {alumno_id} no existe",
        f"No se encontró alumno con el identificador {alumno_id}",
    )


def crear_alumno(alumno_data: AlumnoCreate) -> AlumnoResponse:
    # Si el test envía id, usarlo; si no, generar uno
    if alumno_data.id is not None:
        if _id_existe(alumno_data.id):
            raise ValidationError(
                f"ID {alumno_data.id} ya existe",
                "El ID debe ser único",
            )
        nuevo_id = alumno_data.id
    else:
        nuevo_id = _obtener_siguiente_id()

    # Validar unicidad de matrícula
    if _matricula_existe(alumno_data.matricula):
        logger.error(f"Matrícula duplicada: {alumno_data.matricula}")
        raise ValidationError(
            f"Matrícula {alumno_data.matricula} ya está registrada",
            "La matrícula debe ser única",
        )
    
    nuevo_alumno = {
        "id": nuevo_id,
        "nombres": alumno_data.nombres,
        "apellidos": alumno_data.apellidos,
        "matricula": alumno_data.matricula,
        "promedio": alumno_data.promedio,
    }
    
    alumnos_db.append(nuevo_alumno)
    logger.info(f"Alumno creado: ID {nuevo_id}, matrícula {alumno_data.matricula}")
    
    return AlumnoResponse(**nuevo_alumno)


def actualizar_alumno(alumno_id: int, alumno_data: AlumnoUpdate) -> AlumnoResponse:
    alumno = None
    for a in alumnos_db:
        if a["id"] == alumno_id:
            alumno = a
            break
    
    if alumno is None:
        logger.warning(f"Alumno no encontrado: ID {alumno_id}")
        raise NotFoundError(
            f"Alumno con ID {alumno_id} no existe",
            "No se puede actualizar un alumno inexistente",
        )
    
    if alumno_data.matricula and alumno_data.matricula != alumno["matricula"]:
        if _matricula_existe(alumno_data.matricula, excluir_id=alumno_id):
            logger.error(f"Matrícula duplicada: {alumno_data.matricula}")
            raise ValidationError(
                f"Matrícula {alumno_data.matricula} ya está registrada",
                "La matrícula debe ser única",
            )
    
    if alumno_data.nombres is not None:
        alumno["nombres"] = alumno_data.nombres
    if alumno_data.apellidos is not None:
        alumno["apellidos"] = alumno_data.apellidos
    if alumno_data.matricula is not None:
        alumno["matricula"] = alumno_data.matricula
    if alumno_data.promedio is not None:
        alumno["promedio"] = alumno_data.promedio
    
    logger.info(f"Alumno actualizado: ID {alumno_id}")
    return AlumnoResponse(**alumno)


def eliminar_alumno(alumno_id: int) -> Dict[str, str]:
    global alumnos_db
    
    for i, alumno in enumerate(alumnos_db):
        if alumno["id"] == alumno_id:
            matricula = alumno["matricula"]
            alumnos_db.pop(i)
            logger.info(f"Alumno eliminado: ID {alumno_id}, matrícula {matricula}")
            return {"mensaje": f"Alumno con ID {alumno_id} eliminado correctamente"}
    
    logger.warning(f"Alumno no encontrado: ID {alumno_id}")
    raise NotFoundError(
        f"Alumno con ID {alumno_id} no existe",
        "No se puede eliminar un alumno inexistente",
    )


def obtener_estadisticas() -> Dict[str, Any]:
    if not alumnos_db:
        return {"total": 0, "promedio_general": 0.0}
    
    total = len(alumnos_db)
    promedio_general = sum(a["promedio"] for a in alumnos_db) / total
    
    return {
        "total": total,
        "promedio_general": round(promedio_general, 2),
        "minimo": min(a["promedio"] for a in alumnos_db),
        "maximo": max(a["promedio"] for a in alumnos_db),
    }