from flask import Flask, render_template

app = Flask(__name__)

# =========================
# DATOS DE EJEMPLO
# =========================

matches = [
    {
        "date": "15 Junio 2026",
        "location": "Los Ángeles",
        "teamA": "México",
        "teamB": "Argentina",
        "eloA": 1800,
        "eloB": 1900,
        "probWinA": 35.4,
        "probDraw": 25.1,
        "probWinB": 39.5
    }
]

grupos = {
    "Grupo A": [
        {"name": "México", "ranking": 15},
        {"name": "Sudáfrica", "ranking": 59}
    ],
    "Grupo B": [
        {"name": "Argentina", "ranking": 1},
        {"name": "Francia", "ranking": 2}
    ]
}

equipos = [
    {"name": "México", "ranking": 15},
    {"name": "Argentina", "ranking": 1},
    {"name": "Brasil", "ranking": 3},
    {"name": "Francia", "ranking": 2}
]

# =========================
# RUTAS
# =========================

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/grupos")
def grupos_view():
    return render_template(
        "grupos.html",
        grupos=grupos
    )

@app.route("/fixture")
def fixture():
    return render_template(
        "fixture.html",
        matches=matches
    )

@app.route("/equipos")
def equipos_view():
    return render_template(
        "equipos.html",
        equipos=equipos
    )

@app.route("/predicciones")
def predicciones():
    return render_template("predicciones.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)