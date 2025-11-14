"""
Excepciones personalizadas y manejadores centralizados.

Decisión sobre códigos HTTP:
    - 400 Bad Request: Para errores de validación general
    - 422 Unprocessable Entity: Para errores específicos de Pydantic (alternativa a 400)
    - 404 Not Found: Recurso no existe
    - 409 Conflict: Conflictos de unicidad (e.g., matrícula/numeroEmpleado duplicados)
    - 500 Internal Server Error: Errores no controlados

En este proyecto usamos:
    - 400 para validaciones fallidas (campos inválidos)
    - 404 para recursos no encontrados
    - 500 para errores del servidor
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Optional


class APIException(Exception):
    """Clase base para excepciones de la API."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class ValidationError(APIException):
    """Excepción para errores de validación (400)."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, detail)


class NotFoundError(APIException):
    """Excepción para recurso no encontrado (404)."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, detail)


class ConflictError(APIException):
    """Excepción para conflictos de unicidad (409)."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status.HTTP_409_CONFLICT, detail)


class ServerError(APIException):
    """Excepción para errores del servidor (500)."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, detail)


# Manejadores de excepciones

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Manejo de errores de validación."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Validation Error",
            "message": exc.message,
            "detail": exc.detail,
            "path": str(request.url.path),
        },
    )


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Manejo de recurso no encontrado."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Not Found",
            "message": exc.message,
            "detail": exc.detail,
            "path": str(request.url.path),
        },
    )


async def server_error_handler(request: Request, exc: ServerError) -> JSONResponse:
    """Manejo de errores del servidor."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Internal Server Error",
            "message": exc.message,
            "detail": exc.detail,
            "path": str(request.url.path),
        },
    )