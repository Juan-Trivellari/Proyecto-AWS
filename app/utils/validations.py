"""
Funciones utilitarias de validación (complementarias a Pydantic).

Nota: Pydantic maneja la mayoría de validaciones a través de Field y validators.
Esta módulo proporciona validaciones adicionales de negocio.
"""

from typing import Any, Optional
from .exceptions import ValidationError


def validar_campo_requerido(valor: Any, nombre_campo: str) -> None:
    """
    Validar que un valor no sea None o vacío.
    
    Args:
        valor: Valor a validar
        nombre_campo: Nombre del campo (para el mensaje de error)
    
    Raises:
        ValidationError: Si el valor es None o vacío
    """
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise ValidationError(
            f"Campo requerido: {nombre_campo}",
            f"El campo '{nombre_campo}' no puede estar vacío",
        )


def validar_rango_numerico(
    valor: float,
    minimo: float,
    maximo: float,
    nombre_campo: str,
) -> None:
    """
    Validar que un número esté dentro de un rango.
    
    Args:
        valor: Valor a validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        nombre_campo: Nombre del campo
    
    Raises:
        ValidationError: Si el valor está fuera del rango
    """
    if not (minimo <= valor <= maximo):
        raise ValidationError(
            f"Valor fuera de rango: {nombre_campo}",
            f"El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}",
        )


def validar_formato_matricula(matricula: str) -> None:
    """
    Validar formato de matrícula (AANNNNNN).
    
    Args:
        matricula: Matrícula a validar
    
    Raises:
        ValidationError: Si el formato es inválido
    """
    import re
    if not re.match(r"^[A-Z]{2}[0-9]{6}$", matricula):
        raise ValidationError(
            "Formato de matrícula inválido",
            "Formato esperado: 2 letras mayúsculas + 6 dígitos (ej: AD123456)",
        )


def validar_numero_empleado(numero: str) -> None:
    """
    Validar número de empleado (6 dígitos).
    
    Args:
        numero: Número a validar
    
    Raises:
        ValidationError: Si el formato es inválido
    """
    import re
    if not re.match(r"^\d{6}$", numero):
        raise ValidationError(
            "Formato de número de empleado inválido",
            "Debe ser exactamente 6 dígitos (ej: 789012)",
        )