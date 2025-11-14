"""
Schemas (DTOs) para la entidad Profesor usando Pydantic v2.

Validaciones:
    - id: entero positivo (generado automáticamente)
    - numeroEmpleado: string único, 6 dígitos
    - nombres: string no vacío, 1-100 caracteres
    - apellidos: string no vacío, 1-100 caracteres
    - horasClase: entero positivo, 0-40 horas/semana

Códigos de error:
    - 400/422: Validación fallida
    - 409: Conflicto (numeroEmpleado duplicado)
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProfesorBase(BaseModel):
    """Base schema con campos comunes."""
    
    numeroEmpleado: str = Field(
        ...,
        pattern=r"^\d{6}$",
        description="Número de empleado único (6 dígitos)",
        example="789012",
    )
    nombres: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombres del profesor (1-100 caracteres)",
        example="María",
    )
    apellidos: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Apellidos del profesor (1-100 caracteres)",
        example="Rodríguez Gómez",
    )
    horasClase: int = Field(
        ...,
        ge=0,
        le=40,
        description="Horas de clase por semana (0-40)",
        example=20,
    )

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def nombres_no_vacios(cls, v: str) -> str:
        """Validar que nombres y apellidos no sean vacíos."""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v

    @field_validator("horasClase", mode="before")
    @classmethod
    def validar_horas(cls, v) -> int:
        """Validar que horasClase sea entero."""
        try:
            return int(v)
        except (TypeError, ValueError):
            raise ValueError("Debe ser un número entero entre 0 y 40")


class ProfesorCreate(ProfesorBase):
    """Schema para crear un profesor (POST)."""
    pass


class ProfesorUpdate(BaseModel):
    """Schema para actualizar un profesor (PUT). Todos opcionales."""
    
    numeroEmpleado: Optional[str] = Field(
        None,
        pattern=r"^\d{6}$",
        description="Número de empleado (opcional)",
    )
    nombres: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nombres (opcional)",
    )
    apellidos: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Apellidos (opcional)",
    )
    horasClase: Optional[int] = Field(
        None,
        ge=0,
        le=40,
        description="Horas de clase (opcional)",
    )

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def nombres_no_vacios(cls, v: str) -> str:
        """Validar no vacíos si se proporcionan."""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v


class ProfesorResponse(ProfesorBase):
    """Schema para respuestas (GET)."""
    
    id: int = Field(..., description="ID único del profesor", example=1)

    model_config = {"from_attributes": True}


class ProfesorListResponse(BaseModel):
    """Schema para listar profesores."""
    
    total: int = Field(..., description="Total de profesores", example=3)
    profesores: list[ProfesorResponse] = Field(..., description="Lista de profesores")