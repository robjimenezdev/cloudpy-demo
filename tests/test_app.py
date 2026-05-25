"""
Tests unitarios para Cloudpy Demo API.
Se ejecutan automáticamente en cada push antes del deploy.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app import app, calcular_plan


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Tests de la lógica de negocio ──────────────────────────────────────────

class TestCalcularPlan:

    def test_plan_basico(self):
        resultado = calcular_plan(50)
        assert resultado["plan"] == "Básico"
        assert resultado["precio_iva"] == 69

    def test_plan_esencial(self):
        resultado = calcular_plan(150)
        assert resultado["plan"] == "Esencial"
        assert resultado["precio_iva"] == 99

    def test_plan_profesional(self):
        resultado = calcular_plan(300)
        assert resultado["plan"] == "Profesional"
        assert resultado["precio_iva"] == 149

    def test_plan_empresa(self):
        resultado = calcular_plan(400)
        assert resultado["plan"] == "Empresa"
        assert resultado["precio_iva"] == 229

    def test_limite_exacto_basico(self):
        """100 llamadas exactas → plan Básico, sin exceso."""
        resultado = calcular_plan(100)
        assert resultado["plan"] == "Básico"
        assert resultado["exceso"] == 0

    def test_supera_empresa(self):
        """Más de 500 → Empresa con nota de contacto."""
        resultado = calcular_plan(600)
        assert resultado["plan"] == "Empresa"
        assert resultado["exceso"] == 100
        assert "nota" in resultado


# ── Tests de los endpoints HTTP ────────────────────────────────────────────

class TestEndpoints:

    def test_index(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["estado"] == "ok"
        assert "entorno" in data

    def test_plan_valido(self, client):
        resp = client.get("/plan?llamadas=150")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["plan"] == "Esencial"

    def test_plan_sin_parametro(self, client):
        resp = client.get("/plan?llamadas=0")
        assert resp.status_code == 400

    def test_plan_parametro_invalido(self, client):
        resp = client.get("/plan?llamadas=abc")
        assert resp.status_code == 400

    def test_planes_lista(self, client):
        resp = client.get("/planes")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["planes"]) == 4
class TestDescuento:

    def test_descuento_anual(self, client):
        resp = client.get("/descuento?llamadas=150&meses=12")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["descuento_aplicado"] == "15%"
        assert data["ahorro"] > 0

    def test_sin_descuento_menos_12_meses(self, client):
        resp = client.get("/descuento?llamadas=150&meses=6")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["descuento_aplicado"] == "0%"
        assert data["ahorro"] == 0

    def test_descuento_parametro_invalido(self, client):
        resp = client.get("/descuento?llamadas=abc&meses=12")
        assert resp.status_code == 400

    def test_descuento_llamadas_cero(self, client):
        resp = client.get("/descuento?llamadas=0&meses=12")
        assert resp.status_code == 400