"""
Schemas para Profesor - AJUSTADO PARA TESTS JAVA
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProfesorBase(BaseModel):
    numeroEmpleado: str = Field(..., min_length=1, max_length=20, example="123456")
    nombres: str = Field(..., min_length=1, max_length=100, example="María")
    apellidos: str = Field(..., min_length=1, max_length=100, example="Rodríguez")
    horasClase: int = Field(..., ge=0, le=168, example=20)

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

    @field_validator("horasClase", mode="before")
    @classmethod
    def validar_horas(cls, v) -> int:
        if v is None:
            raise ValueError("Horas no puede ser null")
        
        # Validar que sea entero o float convertible
        if isinstance(v, float):
            # Rechazar floats negativos o fuera de rango
            if v < 0 or v > 168:
                raise ValueError("Horas debe estar entre 0 y 168")
            # Rechazar floats no enteros (ej: -1.26)
            if v != int(v):
                raise ValueError("Horas debe ser un número entero")
            v = int(v)
        
        try:
            val = int(v)
        except (TypeError, ValueError):
            raise ValueError("Horas debe ser un número entero")
        
        if val < 0 or val > 168:
            raise ValueError("Horas debe estar entre 0 y 168")
        return val

    @field_validator("numeroEmpleado", mode="before")
    @classmethod
    def validar_numero(cls, v) -> str:
        if v is None:
            raise ValueError("Número de empleado no puede ser null")
        # Rechazar números negativos directamente
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError("Número de empleado no puede ser negativo")
        # Convertir a string si es número
        v_str = str(v).strip()
        if not v_str or v_str == "-" or v_str.startswith("-"):
            raise ValueError("Número de empleado inválido")
        return v_str


class ProfesorCreate(ProfesorBase):
    """Schema para crear profesor - ACEPTA id opcional"""
    id: Optional[int] = Field(None, description="ID opcional")


class ProfesorUpdate(BaseModel):
    """Schema para actualizar profesor"""
    numeroEmpleado: Optional[str] = Field(None, min_length=1, max_length=20)
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    horasClase: Optional[int] = Field(None, ge=0, le=168)

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

    @field_validator("horasClase", mode="before")
    @classmethod
    def validar_horas(cls, v):
        if v is None:
            raise ValueError("No puede ser null")
        
        # Validar floats
        if isinstance(v, float):
            if v < 0 or v > 168:
                raise ValueError("Debe estar entre 0 y 168")
            if v != int(v):
                raise ValueError("Debe ser un número entero")
            v = int(v)
        
        try:
            val = int(v)
        except (TypeError, ValueError):
            raise ValueError("Debe ser un número entero")
        
        if val < 0 or val > 168:
            raise ValueError("Debe estar entre 0 y 168")
        return val

    @field_validator("numeroEmpleado", mode="before")
    @classmethod
    def validar_numero(cls, v):
        if v is None:
            raise ValueError("No puede ser null")
        # Rechazar números negativos
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError("Número de empleado no puede ser negativo")
        v_str = str(v).strip()
        if not v_str or v_str.startswith("-"):
            raise ValueError("Número inválido")
        return v_str


class ProfesorResponse(ProfesorBase):
    id: int = Field(..., example=1)

    model_config = {"from_attributes": True}