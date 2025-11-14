"""
Punto de entrada principal de la aplicación FastAPI.

Ejecutar desde la raíz del proyecto con:
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.routes import alumnos, profesores
from app.utils.exceptions import (
    ValidationError,
    NotFoundError,
    ServerError,
    validation_error_handler,
    not_found_error_handler,
    server_error_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API REST - Gestión de Alumnos y Profesores",
    description="API REST educativa con persistencia en memoria. ⚠️ Los datos se pierden al reiniciar.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(ServerError, server_error_handler)

app.include_router(alumnos.router, prefix="/alumnos", tags=["Alumnos"])
app.include_router(profesores.router, prefix="/profesores", tags=["Profesores"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "mensaje": "Bienvenido a la API REST de Gestión Educativa",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "advertencia": "⚠️ Persistencia solo en memoria - los datos se pierden al reiniciar",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "API REST - Proyecto Educativo",
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando servidor FastAPI...")
    logger.info("📚 Documentación: http://localhost:8000/docs")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )