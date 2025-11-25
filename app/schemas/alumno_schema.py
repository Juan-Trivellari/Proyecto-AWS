"""
Schemas para Alumno - AJUSTADO PARA TESTS JAVA
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AlumnoBase(BaseModel):
    nombres: str = Field(..., min_length=1, max_length=100, example="Juan")
    apellidos: str = Field(..., min_length=1, max_length=100, example="García")
    matricula: str = Field(..., min_length=1, max_length=50, example="A123456")
    promedio: float = Field(..., ge=0.0, le=5.0, example=4.25)

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def validar_no_vacio(cls, v: str) -> str:
        if v is None:
            raise ValueError("No puede ser null")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v

    @field_validator("promedio", mode="before")
    @classmethod
    def validar_promedio(cls, v) -> float:
        if v is None:
            raise ValueError("Promedio no puede ser null")
        try:
            val = float(v)
        except (TypeError, ValueError):
            raise ValueError("Promedio debe ser un número válido")
        
        if val < 0.0 or val > 5.0:
            raise ValueError("Promedio debe estar entre 0.0 y 5.0")
        return val

    @field_validator("matricula", mode="before")
    @classmethod
    def validar_matricula(cls, v) -> str:
        if v is None:
            raise ValueError("Matrícula no puede ser null")
        # Rechazar floats/doubles (valores como -1.223)
        if isinstance(v, float):
            raise ValueError("Matrícula no puede ser un número decimal")
        # Convertir int a string si es necesario
        if isinstance(v, int):
            v = str(v)
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Matrícula debe ser un string no vacío")
        return v.strip()


class AlumnoCreate(AlumnoBase):
    """Schema para crear alumno - ACEPTA id opcional"""
    id: Optional[int] = Field(None, description="ID opcional (si no se envía, se genera)")


class AlumnoUpdate(BaseModel):
    """Schema para actualizar alumno"""
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    matricula: Optional[str] = Field(None, min_length=1, max_length=50)
    promedio: Optional[float] = Field(None, ge=0.0, le=5.0)

    @field_validator("nombres", "apellidos", mode="before")
    @classmethod
    def validar_no_vacio(cls, v):
        if v is None:
            raise ValueError("No puede ser null")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("No puede estar vacío")
        return v

    @field_validator("promedio", mode="before")
    @classmethod
    def validar_promedio(cls, v):
        if v is None:
            raise ValueError("No puede ser null")
        try:
            val = float(v)
        except (TypeError, ValueError):
            raise ValueError("Debe ser un número válido")
        
        if val < 0.0 or val > 5.0:
            raise ValueError("Debe estar entre 0.0 y 5.0")
        return val

    @field_validator("matricula", mode="before")
    @classmethod
    def validar_matricula(cls, v):
        if v is None:
            raise ValueError("No puede ser null")
        # Rechazar floats/doubles
        if isinstance(v, float):
            raise ValueError("Matrícula no puede ser un número decimal")
        # Convertir int a string
        if isinstance(v, int):
            v = str(v)
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Debe ser string no vacío")
        return v.strip()


class AlumnoResponse(AlumnoBase):
    id: int = Field(..., example=1)

    model_config = {"from_attributes": True}