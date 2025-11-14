"""
Tests de integración.
Ejecutar: pytest -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAlumnos:
    def test_listar_alumnos(self):
        response = client.get("/alumnos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_alumno_valido(self):
        payload = {
            "nombres": "Juan",
            "apellidos": "García López",
            "matricula": "AD123456",
            "promedio": 4.25,
        }
        response = client.post("/alumnos", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["nombres"] == "Juan"
        assert data["matricula"] == "AD123456"
        assert "id" in data


class TestProfesores:
    def test_listar_profesores(self):
        response = client.get("/profesores")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_crear_profesor_valido(self):
        payload = {
            "numeroEmpleado": "789012",
            "nombres": "María",
            "apellidos": "Rodríguez",
            "horasClase": 20,
        }
        response = client.post("/profesores", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["numeroEmpleado"] == "789012"
        assert "id" in data