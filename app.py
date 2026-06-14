from flask import Flask, render_template, jsonify, request
from typing import Any
import webbrowser
from threading import Timer

app = Flask(__name__)

# Base de datos limpia de los Grupos y sus Equipos participantes
GRUPOS_MUNDIAL: dict[str, list[dict[str, Any]]] = {
    "Grupo A": [
        {"name": "México", "flag": "static/img/mexico.png", "ranking": 15, "top_scorer": "Santiago Giménez"},
        {"name": "Sudáfrica", "flag": "static/img/sudafrica.png", "ranking": 59, "top_scorer": "Percy Tau"},
        {"name": "Corea del Sur", "flag": "static/img/corea.png", "ranking": 22, "top_scorer": "Son Heung-min"},
    ],
    "Grupo I": [
        {"name": "Francia", "flag": "static/img/francia.png", "ranking": 2, "top_scorer": "Kylian Mbappé"},
    ],
    "Grupo J": [
        {"name": "Argentina", "flag": "static/img/argentina.png", "ranking": 1, "top_scorer": "Lionel Messi"},
    ]
}

# Calendario de partidos con probabilidades estadísticas de ganar (Estilo ELO)
PARTIDOS: list[dict[str, Any]] = [
    {
        "date": "25 JUN 2026",
        "location": "Ciudad de México",
        "teamA": "México",
        "teamB": "Sudáfrica",
        "eloA": 1875,
        "eloB": 1518,
        "probWinA": 79.7,
        "probDraw": 10.1,
        "probWinB": 10.2
    }
]


def analizar_consulta_ia(pregunta: str) -> str:
    """Procesa e interpreta las preguntas del usuario sobre el torneo."""
    query = pregunta.lower().strip()
    if not query:
        return "¡Hola! Hazme una pregunta sobre los grupos o las probabilidades de los partidos."

    if "méxico" in query or "mexico" in query:
        match = PARTIDOS[0]
        return (f"México (Elo {match['eloA']}) se enfrenta a Sudáfrica el {match['date']}. "
                f"Tiene un dominante {match['probWinA']}% de probabilidad de victoria según el modelo matemático.")
    
    if "grupo a" in query:
        return "El Grupo A está compuesto por México, Sudáfrica, Corea del Sur y el clasificado de la UEFA 4."

    return "Como IA del Mundial, veo que este torneo de 48 equipos está muy reñido. ¿Quieres saber el porcentaje de victoria de algún partido en específico?"


@app.route("/")
def home() -> str:
    """Renderiza la vista principal dividida del portal."""
    return render_template("index.html", grupos=GRUPOS_MUNDIAL, matches=PARTIDOS)


@app.route("/ask", methods=["POST"])
def ask() -> Any:
    """Endpoint API para responder dudas mediante la IA."""
    data = request.get_json(silent=True) or {}
    pregunta = data.get("question", "")
    respuesta = analizar_consulta_ia(pregunta)
    return jsonify({"answer": respuesta})


def abrir_navegador() -> None:
    """Abre el navegador predeterminado en la dirección local del servidor."""
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Espera 1 segundo de forma asíncrona para dar tiempo a que Flask levante el entorno,
    # y luego ejecuta la función para abrir el navegador de forma automática.
    Timer(1.0, abrir_navegador).start()
    
    # Desactivamos 'use_reloader' para evitar que abra duplicados al reiniciar el proceso de debug.
    app.run(debug=True, use_reloader=False)