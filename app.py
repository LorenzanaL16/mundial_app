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
    ],

"Grupo E": [
    {"name": "Alemania", "ranking": 10},
    {"name": "Curazao", "ranking": 90},
    {"name": "Costa de Marfil", "ranking": 41},
    {"name": "Ecuador", "ranking": 24}
    ],

"Grupo F": [
    {"name": "Países Bajos", "ranking": 7},
    {"name": "Japón", "ranking": 17},
    {"name": "Suecia", "ranking": 28},
    {"name": "Túnez", "ranking": 49}
    ],

"Grupo G": [
    {"name": "Bélgica", "ranking": 8},
    {"name": "Egipto", "ranking": 36},
    {"name": "Irán", "ranking": 20},
    {"name": "Nueva Zelanda", "ranking": 94}
    ],

"Grupo H": [
    {"name": "España", "ranking": 3},
    {"name": "Cabo Verde", "ranking": 72},
    {"name": "Arabia Saudita", "ranking": 58},
    {"name": "Uruguay", "ranking": 13}
    ],

"Grupo I": [
    {"name": "Francia", "ranking": 2},
    {"name": "Senegal", "ranking": 18},
    {"name": "Irak", "ranking": 58},
    {"name": "Noruega", "ranking": 43}
],

"Grupo J": [
    {"name": "Argentina", "ranking": 1},
    {"name": "Argelia", "ranking": 37},
    {"name": "Austria", "ranking": 22},
    {"name": "Jordania", "ranking": 64}
],

"Grupo K": [
    {"name": "Portugal", "ranking": 6},
    {"name": "República Democrática del Congo", "ranking": 61},
    {"name": "Uzbekistán", "ranking": 57},
    {"name": "Colombia", "ranking": 14}
],

"Grupo L": [
    {"name": "Inglaterra", "ranking": 4},
    {"name": "Croacia", "ranking": 11},
    {"name": "Ghana", "ranking": 76},
    {"name": "Panamá", "ranking": 44}
],
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