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
        {"name": "Sudáfrica", "ranking": 59},
        {"name": "Corea del Sur", "ranking": 23},
        {"name": "República Checa", "ranking": 42}
    ],

    "Grupo B": [
        {"name": "Canadá", "ranking": 31},
        {"name": "Bosnia y Herzegovina", "ranking": 74},
        {"name": "Qatar", "ranking": 55},
        {"name": "Suiza", "ranking": 20}
    ],

    "Grupo C": [
        {"name": "Brasil", "ranking": 3},
        {"name": "Marruecos", "ranking": 12},
        {"name": "Haití", "ranking": 83},
        {"name": "Escocia", "ranking": 28}
    ],

    "Grupo D": [
        {"name": "Estados Unidos", "ranking": 16},
        {"name": "Paraguay", "ranking": 53},
        {"name": "Australia", "ranking": 24},
        {"name": "Turquía", "ranking": 35}
    ]
}

equipos = []

for grupo, lista in grupos.items():
    for equipo in lista:
        equipo["group"] = grupo
        equipos.append(equipo)

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