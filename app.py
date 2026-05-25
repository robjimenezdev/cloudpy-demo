"""
Cloudpy Demo API
Calcula el plan óptimo según número de llamadas mensuales.
"""

import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# El entorno viene de una variable de entorno (DEV / STAGING / PROD)
ENVIRONMENT = os.getenv("APP_ENV", "DEV")

PLANES = {
    "basico":       {"llamadas": 100, "precio": 69,  "label": "Básico"},
    "esencial":     {"llamadas": 200, "precio": 99,  "label": "Esencial"},
    "profesional":  {"llamadas": 300, "precio": 149, "label": "Profesional"},
    "empresa":      {"llamadas": 500, "precio": 229, "label": "Empresa"},
}


def calcular_plan(llamadas: int) -> dict:
    """Devuelve el plan más ajustado para el número de llamadas dado."""
    for key, plan in PLANES.items():
        if llamadas <= plan["llamadas"]:
            return {
                "plan": plan["label"],
                "llamadas_incluidas": plan["llamadas"],
                "precio_iva": plan["precio"],
                "exceso": max(0, llamadas - plan["llamadas"]),
            }
    # Si supera todos los planes, devuelve el máximo
    plan = PLANES["empresa"]
    return {
        "plan": plan["label"],
        "llamadas_incluidas": plan["llamadas"],
        "precio_iva": plan["precio"],
        "exceso": llamadas - plan["llamadas"],
        "nota": "Contacta con nosotros para un plan personalizado",
    }


@app.route("/")
def index():
    return jsonify({
        "servicio": "Cloudpy Agenda Llamadas",
        "version": "1.0.0",
        "entorno": ENVIRONMENT,
        "estado": "ok",
    })


@app.route("/plan")
def plan():
    """
    GET /plan?llamadas=150
    Devuelve el plan recomendado para ese número de llamadas.
    """
    try:
        llamadas = int(request.args.get("llamadas", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "El parámetro 'llamadas' debe ser un número entero"}), 400

    if llamadas <= 0:
        return jsonify({"error": "El número de llamadas debe ser mayor que 0"}), 400

    resultado = calcular_plan(llamadas)
    resultado["entorno"] = ENVIRONMENT
    return jsonify(resultado)


@app.route("/planes")
def planes():
    """GET /planes — Lista todos los planes disponibles."""
    return jsonify({
        "entorno": ENVIRONMENT,
        "planes": [
            {
                "id": key,
                "label": p["label"],
                "llamadas": p["llamadas"],
                "precio_iva": p["precio"],
            }
            for key, p in PLANES.items()
        ],
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = ENVIRONMENT == "DEV"
    app.run(host="0.0.0.0", port=port, debug=debug)
