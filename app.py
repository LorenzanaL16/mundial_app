from flask import Flask, render_template, request, jsonify
import re
import unicodedata

app = Flask(__name__)

# =========================
# NORMALIZAR
# =========================
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r"[¿?¡!.,]", "", texto)
    return texto

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
        {"name": "México", "ranking": 15,"flag": "img/flags/mexico.png"},
        {"name": "Sudáfrica", "ranking": 59, "flag": "img/flags/sudafrica.png"},
        {"name": "Corea del Sur", "ranking": 23, "flag": "img/flags/corea-del-sur.png"},
        {"name": "República Checa", "ranking": 42, "flag": "img/flags/republica-checa.png"}
    ],

    "Grupo B": [
        {"name": "Canadá", "ranking": 31, "flag": "img/flags/canada.png"},
        {"name": "Bosnia y Herzegovina", "ranking": 74, "flag": "img/flags/bosnia-y-herzegovina.png"},
        {"name": "Qatar", "ranking": 55, "flag": "img/flags/qatar.png"},
        {"name": "Suiza", "ranking": 20, "flag": "img/flags/suiza.png"}
    ],

    "Grupo C": [
        {"name": "Brasil", "ranking": 3, "flag": "img/flags/brasil.png"},
        {"name": "Marruecos", "ranking": 12, "flag": "img/flags/marruecos.png"},
        {"name": "Haití", "ranking": 83, "flag": "img/flags/haiti.png"},
        {"name": "Escocia", "ranking": 28, "flag": "img/flags/escocia.png"}
    ],

    "Grupo D": [
        {"name": "Estados Unidos", "ranking": 16, "flag": "img/flags/estados-unidos.png"},
        {"name": "Paraguay", "ranking": 53, "flag": "img/flags/paraguay.png"},
        {"name": "Australia", "ranking": 24, "flag": "img/flags/australia.png"},
        {"name": "Turquía", "ranking": 35, "flag": "img/flags/turquia.png"}
    ],

"Grupo E": [
    {"name": "Alemania", "ranking": 10, "flag": "img/flags/alemania.png"},
    {"name": "Curazao", "ranking": 90, "flag": "img/flags/curazao.png"},
    {"name": "Costa de Marfil", "ranking": 41, "flag": "img/flags/costa-de-marfil.png"},
    {"name": "Ecuador", "ranking": 24, "flag": "img/flags/ecuador.png"}
    ],

"Grupo F": [
    {"name": "Países Bajos", "ranking": 7, "flag": "img/flags/paises-bajos.png"},
    {"name": "Japón", "ranking": 17, "flag": "img/flags/japon.png"},
    {"name": "Suecia", "ranking": 28, "flag": "img/flags/suecia.png"},
    {"name": "Túnez", "ranking": 49, "flag": "img/flags/tunez.png"}
    ],

"Grupo G": [
    {"name": "Bélgica", "ranking": 8, "flag": "img/flags/belgica.png"},
    {"name": "Egipto", "ranking": 36, "flag": "img/flags/egipto.png"},
    {"name": "Irán", "ranking": 20, "flag": "img/flags/iran.png"},
    {"name": "Nueva Zelanda", "ranking": 94, "flag": "img/flags/nueva-zelanda.png"}
    ],

"Grupo H": [
    {"name": "España", "ranking": 3, "flag": "img/flags/espana.png"},
    {"name": "Cabo Verde", "ranking": 72, "flag": "img/flags/cabo-verde.png"},
    {"name": "Arabia Saudita", "ranking": 58, "flag": "img/flags/arabia-saudita.png"},
    {"name": "Uruguay", "ranking": 13, "flag": "img/flags/uruguay.png"}
    ],

"Grupo I": [
    {"name": "Francia", "ranking": 2, "flag": "img/flags/francia.png"},
    {"name": "Senegal", "ranking": 18, "flag": "img/flags/senegal.png"},
    {"name": "Irak", "ranking": 58, "flag": "img/flags/irak.png"},
    {"name": "Noruega", "ranking": 43, "flag": "img/flags/noruega.png"}
],

"Grupo J": [
    {"name": "Argentina", "ranking": 1, "flag": "img/flags/argentina.png"},
    {"name": "Argelia", "ranking": 37, "flag": "img/flags/argelia.png"},
    {"name": "Austria", "ranking": 22, "flag": "img/flags/austria.png"},
    {"name": "Jordania", "ranking": 64, "flag": "img/flags/jordania.png"}
],

"Grupo K": [
    {"name": "Portugal", "ranking": 6, "flag": "img/flags/portugal.png"},
    {"name": "República Democrática del Congo", "ranking": 61, "flag": "img/flags/rd-congo.png"},
    {"name": "Uzbekistán", "ranking": 57, "flag": "img/flags/uzbekistan.png"},
    {"name": "Colombia", "ranking": 14, "flag": "img/flags/colombia.png"}
],

"Grupo L": [
    {"name": "Inglaterra", "ranking": 4, "flag": "img/flags/inglaterra.png"},
    {"name": "Croacia", "ranking": 11, "flag": "img/flags/croacia.png"},
    {"name": "Ghana", "ranking": 76, "flag": "img/flags/ghana.png"},
    {"name": "Panamá", "ranking": 44, "flag": "img/flags/panama.png"}
],
}

# =========================
# INTENCIONES
# =========================

def detectar_intencion(p):

    if any(x in p for x in ["cuando juega", "cuándo juega", "partido", "fixture"]):
        return "fixture"

    if any(x in p for x in ["grupo"]):
        return "grupo"

    if any(x in p for x in ["ranking"]):
        return "ranking"

    if any(x in p for x in ["favorito", "ganara", "ganará"]):
        return "favorito"

    return "general"

def responder_chatbot(pregunta):

    p = normalizar(pregunta)

    intent = detectar_intencion(p)

 # =========================
    # FIXTURE / PARTIDOS
    # =========================
    if intent == "fixture":

        for match in matches:
            if match["teamA"].lower() in p or match["teamB"].lower() in p:

                return (
                    f"📅 El partido {match['teamA']} vs {match['teamB']} "
                    f"se jugará el {match['date']} en {match['location']}. "
                    f"⚽ Según el modelo: {match['teamA']} {match['probWinA']}% | "
                    f"Empate {match['probDraw']}% | {match['teamB']} {match['probWinB']}%"
                )

        return "No encontré ese partido en el fixture, pero puedo mostrarte los juegos disponibles."
    
    # =========================
    # EQUIPOS
    # =========================
    if intent == "general":
        if "cuantos equipos" in p:
            return "El Mundial 2026 tendrá 48 equipos participantes."

    # =========================
    # RANKING
    # =========================
    if intent == "ranking":
        for equipo in equipos:
            nombre = normalizar(equipo["name"])
            if nombre in p:
                return f"{equipo['name']} está en el ranking FIFA #{equipo['ranking']}."
        return "Dime el nombre de un equipo para darte su ranking."

    # =========================
    # GRUPOS
    # =========================
    if intent == "grupo":
        for grupo, lista in grupos.items():
            for equipo in lista:
                nombre = normalizar(equipo["name"])
                if nombre in p:
                    return f"{equipo['name']} pertenece al {grupo}."

        return "Dime un equipo para decirte su grupo."

    # =====================
    # FIXTURE
    # =====================
    if intent == "fixture":
        for match in matches:
            if normalizar(match["teamA"]) in p or normalizar(match["teamB"]) in p:
                return f"{match['teamA']} vs {match['teamB']} juega el {match['date']} en {match['location']}."

        return "No tengo información de ese partido en el fixture."

    # =========================
    # FAVORITO
    # =========================
    if intent == "favorito":
        return "Argentina, Brasil y Francia son los principales favoritos según el modelo."
    
      # =========================
    # GENERAL (IA STYLE)
    # =========================
    return (
        "🤖 No estoy seguro de eso todavía.\n\n"
        "Puedes preguntarme sobre:\n"
        "• Partidos del Mundial (fixture)\n"
        "• Grupos\n"
        "• Ranking FIFA\n"
        "• Favoritos del torneo"
    )

    # =========================
    # PRECISIÓN
    # =========================
    if "accuracy" in p or "preciso" in p:
        return "El modelo tiene 58.4% accuracy y 55.1% F1-score."

    # =========================
    # DEFAULT
    # =========================
    return "No entendí tu pregunta 🤔. Puedes preguntarme sobre equipos, grupos, partidos o rankings del Mundial 2026."
# =========================
# RUTAS WEB
# =========================

@app.route("/grupos")
def grupos_view():
    return render_template("grupos.html", grupos=grupos)

@app.route("/fixture")
def fixture():
    return render_template("fixture.html", matches=matches, flags=flags)

@app.route("/equipos")
def equipos_view():
    return render_template("equipos.html", equipos=equipos)

@app.route("/predicciones")
def predicciones():
    return render_template("predicciones.html")

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/chatbot", methods=["GET"])
def chatbot_page():
    return render_template("chatbot.html")

# =========================
# API (TIEMPO REAL)
# =========================

@app.route("/api/chatbot", methods=["POST"])
def api_chatbot():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    respuesta = responder_chatbot(pregunta)

    return jsonify({"respuesta": respuesta})

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)