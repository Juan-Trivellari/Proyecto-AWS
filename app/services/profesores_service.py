"""
Servicio CRUD para Profesores - AJUSTADO PARA TESTS
"""

from typing import Optional, List, Dict, Any
from app.schemas.profesor_schema import ProfesorCreate, ProfesorUpdate, ProfesorResponse
from app.utils.exceptions import ValidationError, NotFoundError
import logging

logger = logging.getLogger(__name__)

profesores_db: List[Dict[str, Any]] = []
_next_profesor_id: int = 1


def _obtener_siguiente_id() -> int:
    global _next_profesor_id
    id_actual = _next_profesor_id
    _next_profesor_id += 1
    return id_actual


def _numero_empleado_existe(numero: str, excluir_id: Optional[int] = None) -> bool:
    for profesor in profesores_db:
        if profesor["numeroEmpleado"] == numero:
            if excluir_id is None or profesor["id"] != excluir_id:
                return True
    return False


def _id_existe(id: int) -> bool:
    for profesor in profesores_db:
        if profesor["id"] == id:
            return True
    return False


def obtener_todos_profesores() -> List[ProfesorResponse]:
    logger.info(f"Obteniendo {len(profesores_db)} profesores")
    return [ProfesorResponse(**profesor) for profesor in profesores_db]


def obtener_profesor_por_id(profesor_id: int) -> ProfesorResponse:
    for profesor in profesores_db:
        if profesor["id"] == profesor_id:
            logger.info(f"Profesor encontrado: ID {profesor_id}")
            return ProfesorResponse(**profesor)
    
    logger.warning(f"Profesor no encontrado: ID {profesor_id}")
    raise NotFoundError(
        f"Profesor con ID {profesor_id} no existe",
        f"No se encontró profesor con el identificador {profesor_id}",
    )


def crear_profesor(profesor_data: ProfesorCreate) -> ProfesorResponse:
    # Si el test envía id, usarlo
    if profesor_data.id is not None:
        if _id_existe(profesor_data.id):
            raise ValidationError(
                f"ID {profesor_data.id} ya existe",
                "El ID debe ser único",
            )
        nuevo_id = profesor_data.id
    else:
        nuevo_id = _obtener_siguiente_id()

    # Validar unicidad de numeroEmpleado
    if _numero_empleado_existe(profesor_data.numeroEmpleado):
        logger.error(f"Número duplicado: {profesor_data.numeroEmpleado}")
        raise ValidationError(
            f"Número de empleado {profesor_data.numeroEmpleado} ya existe",
            "El número de empleado debe ser único",
        )
    
    nuevo_profesor = {
        "id": nuevo_id,
        "numeroEmpleado": profesor_data.numeroEmpleado,
        "nombres": profesor_data.nombres,
        "apellidos": profesor_data.apellidos,
        "horasClase": profesor_data.horasClase,
    }
    
    profesores_db.append(nuevo_profesor)
    logger.info(f"Profesor creado: ID {nuevo_id}")
    
    return ProfesorResponse(**nuevo_profesor)


def actualizar_profesor(profesor_id: int, profesor_data: ProfesorUpdate) -> ProfesorResponse:
    profesor = None
    for p in profesores_db:
        if p["id"] == profesor_id:
            profesor = p
            break
    
    if profesor is None:
        logger.warning(f"Profesor no encontrado: ID {profesor_id}")
        raise NotFoundError(
            f"Profesor con ID {profesor_id} no existe",
            "No se puede actualizar un profesor inexistente",
        )
    
    if profesor_data.numeroEmpleado and profesor_data.numeroEmpleado != profesor["numeroEmpleado"]:
        if _numero_empleado_existe(profesor_data.numeroEmpleado, excluir_id=profesor_id):
            logger.error(f"Número duplicado: {profesor_data.numeroEmpleado}")
            raise ValidationError(
                f"Número de empleado {profesor_data.numeroEmpleado} ya existe",
                "El número debe ser único",
            )
    
    if profesor_data.numeroEmpleado is not None:
        profesor["numeroEmpleado"] = profesor_data.numeroEmpleado
    if profesor_data.nombres is not None:
        profesor["nombres"] = profesor_data.nombres
    if profesor_data.apellidos is not None:
        profesor["apellidos"] = profesor_data.apellidos
    if profesor_data.horasClase is not None:
        profesor["horasClase"] = profesor_data.horasClase
    
    logger.info(f"Profesor actualizado: ID {profesor_id}")
    return ProfesorResponse(**profesor)


def eliminar_profesor(profesor_id: int) -> Dict[str, str]:
    global profesores_db
    
    for i, profesor in enumerate(profesores_db):
        if profesor["id"] == profesor_id:
            numero = profesor["numeroEmpleado"]
            profesores_db.pop(i)
            logger.info(f"Profesor eliminado: ID {profesor_id}")
            return {"mensaje": f"Profesor con ID {profesor_id} eliminado correctamente"}
    
    logger.warning(f"Profesor no encontrado: ID {profesor_id}")
    raise NotFoundError(
        f"Profesor con ID {profesor_id} no existe",
        "No se puede eliminar un profesor inexistente",
    )


def obtener_estadisticas() -> Dict[str, Any]:
    if not profesores_db:
        return {"total": 0, "promedio_horas": 0.0}
    
    total = len(profesores_db)
    promedio_horas = sum(p["horasClase"] for p in profesores_db) / total
    total_horas = sum(p["horasClase"] for p in profesores_db)
    
    return {
        "total": total,
        "promedio_horas": round(promedio_horas, 1),
        "total_horas": total_horas,
        "minimo_horas": min(p["horasClase"] for p in profesores_db),
        "maximo_horas": max(p["horasClase"] for p in profesores_db),
    }