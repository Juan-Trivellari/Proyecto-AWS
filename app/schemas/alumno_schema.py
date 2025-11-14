"""
Schemas (DTOs) para la entidad Alumno usando Pydantic v2.

Validaciones:
    - id: entero positivo (generado automáticamente por el servicio)
    - nombres: string no vacío, 1-100 caracteres
    - apellidos: string no vacío, 1-100 caracteres
    - matricula: string único, formato: [A-Z]{2}[0-9]{6}
    - promedio: float en rango [0.0, 5.0]

Códigos de error:
    - 400: Si algún campo no cumple validaciones
    - 422: Si la validación falla en Pydantic (alternativa a 400)
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AlumnoBase(BaseModel):
    """Base schema con campos comunes."""
    
    nombres: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombres del alumno (1-100 caracteres)",
        example="Juan Carlos",
    )
    apellidos: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Apellidos del alumno (1-100 caracteres)",
        example="García López",
    )
    matricula: str = Field(
        ...,
        pattern=r"^[A-Z]{2}[0-9]{6}$",
        description="Matrícula única en formato AANNNNNN",
        example="AD123456",
    )
    promedio: float = Field(
        ...,
        ge=0.0,
        le=5.0,
        description="Promedio académico (0.0 a 5.0)",
        example=4.25,
    )

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def nombres_no_vacios(cls, v: str) -> str:
        """Validar que nombres y apellidos no sean strings vacíos."""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v

    @field_validator("promedio", mode="before")
    @classmethod
    def validar_promedio(cls, v) -> float:
        """Validar que promedio sea numérico."""
        try:
            return float(v)
        except (TypeError, ValueError):
            raise ValueError("Debe ser un número válido entre 0.0 y 5.0")


class AlumnoCreate(AlumnoBase):
    """Schema para crear un alumno (POST)."""
    pass


class AlumnoUpdate(BaseModel):
    """Schema para actualizar un alumno (PUT). Todos los campos opcionales."""
    
    nombres: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nombres del alumno (opcional)",
    )
    apellidos: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Apellidos del alumno (opcional)",
    )
    matricula: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}[0-9]{6}$",
        description="Matrícula única (opcional)",
    )
    promedio: Optional[float] = Field(
        None,
        ge=0.0,
        le=5.0,
        description="Promedio académico (opcional)",
    )

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def nombres_no_vacios(cls, v: str) -> str:
        """Validar que no sean strings vacíos si se proporcionan."""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v


class AlumnoResponse(AlumnoBase):
    """Schema para respuestas (GET). Incluye id."""
    
    id: int = Field(..., description="ID único del alumno generado por el servidor", example=1)

    model_config = {"from_attributes": True}


class AlumnoListResponse(BaseModel):
    """Schema para listar alumnos."""
    
    total: int = Field(..., description="Total de alumnos", example=5)
    alumnos: list[AlumnoResponse] = Field(..., description="Lista de alumnos")