from flask import Flask, render_template, request, jsonify
import re
import unicodedata
import sqlite3
import io
import csv
from flask import Response

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

equipos = []

for grupo, lista in grupos.items():
    for equipo in lista:
        equipo["group"] = grupo
        equipos.append(equipo)

matches = []

fechas = ["15 Junio 2026", "20 Junio 2026", "25 Junio 2026"]

for grupo, equipos_lista in grupos.items():

    for jornada, pares in enumerate([
        [(0,1), (2,3)],
        [(0,2), (1,3)],
        [(0,3), (1,2)]
    ]):

        for i, j in pares:

            equipoA = equipos_lista[i]
            equipoB = equipos_lista[j]

            eloA = equipoA["ranking"] * 10
            eloB = equipoB["ranking"] * 10

            probA = round(50 + (eloB - eloA) * 0.05, 1)
            probB = round(50 + (eloA - eloB) * 0.05, 1)

            probA = max(5, min(90, probA))
            probB = max(5, min(90, probB))
            probD = round(100 - (probA + probB), 1)

            matches.append({
                "grupo": grupo,
                "date": fechas[jornada],
                "location": "Sede Mundial 2026",
                "teamA": equipoA["name"],
                "teamB": equipoB["name"],
                "eloA": eloA,
                "eloB": eloB,
                "probWinA": probA,
                "probDraw": probD,
                "probWinB": probB
            })
            
flags = {}

for equipo in equipos:
    flags[equipo["name"]] = equipo["flag"]


def buscar_equipo_por_nombre(nombre):
    clave = normalizar(nombre)
    for equipo in equipos:
        if normalizar(equipo["name"]) == clave:
            return equipo
    return None


def obtener_ganador_grupo(grupo):
    lista = grupos.get(grupo)
    if not lista:
        return None
    ganador = min(lista, key=lambda x: x["ranking"])
    return ganador["name"]


def clasificados_por_grupo():
    resultado = {}
    for grupo, lista in grupos.items():
        orden = sorted(lista, key=lambda x: x["ranking"])
        resultado[grupo] = {"1ro": orden[0]["name"], "2do": orden[1]["name"]}
    return resultado


def mundiales_ganados(nombre):
    datos = {
        "brasil": 5,
        "alemania": 4,
        "italia": 4,
        "argentina": 3,
        "uruguay": 2,
        "francia": 2,
        "inglaterra": 1,
        "españa": 1,
    }
    equipo = buscar_equipo_por_nombre(nombre)
    if equipo:
        return datos.get(normalizar(equipo["name"]))
    return datos.get(normalizar(nombre))


def calcular_tabla_posiciones():
    import random

    tabla = {
        grupo: {
            equipo["name"]: {"pts": 0, "pj": 0, "gf": 0, "gc": 0, "dg": 0}
            for equipo in lista
        }
        for grupo, lista in grupos.items()
    }

    matches_with_scores = []

    for match in matches:
        grupo = match.get("grupo")
        if grupo not in tabla:
            continue

        local = match["teamA"]
        visitante = match["teamB"]
        probA = float(match.get("probWinA", 0) or 0)
        probB = float(match.get("probWinB", 0) or 0)
        probD = float(match.get("probDraw", 0) or 0)

        total = probA + probB + probD
        if total <= 0:
            probA, probB, probD = 0.33, 0.33, 0.34
        else:
            probA /= total
            probB /= total
            probD /= total

        seed = f"{local}-{visitante}-{probA:.4f}-{probB:.4f}-{probD:.4f}"
        rnd = random.Random(seed)
        r = rnd.random()

        if r < probA:
            gl = rnd.randint(2, 4)
            gv = rnd.randint(1, gl - 1)
        elif r < probA + probD:
            gl = gv = rnd.randint(1, 3)
        else:
            gv = rnd.randint(2, 4)
            gl = rnd.randint(1, gv - 1)

        matches_with_scores.append({
            "grupo": grupo,
            "local": local,
            "visitante": visitante,
            "gl": gl,
            "gv": gv
        })

    stats = {
        grupo: {
            equipo: {"pts": 0, "pj": 0, "gf": 0, "gc": 0, "dg": 0}
            for equipo in equipos_grupo
        }
        for grupo, equipos_grupo in tabla.items()
    }

    def compute_stats():
        for grupo, equipos_grupo in stats.items():
            for equipo in equipos_grupo:
                stats[grupo][equipo] = {"pts": 0, "pj": 0, "gf": 0, "gc": 0, "dg": 0}

        for match_data in matches_with_scores:
            grupo = match_data["grupo"]
            local = match_data["local"]
            visitante = match_data["visitante"]
            gl = match_data["gl"]
            gv = match_data["gv"]

            if local not in stats[grupo]:
                stats[grupo][local] = {"pts": 0, "pj": 0, "gf": 0, "gc": 0, "dg": 0}
            if visitante not in stats[grupo]:
                stats[grupo][visitante] = {"pts": 0, "pj": 0, "gf": 0, "gc": 0, "dg": 0}

            stats[grupo][local]["pj"] += 1
            stats[grupo][visitante]["pj"] += 1
            stats[grupo][local]["gf"] += gl
            stats[grupo][local]["gc"] += gv
            stats[grupo][visitante]["gf"] += gv
            stats[grupo][visitante]["gc"] += gl

            if gl > gv:
                stats[grupo][local]["pts"] += 3
            elif gl < gv:
                stats[grupo][visitante]["pts"] += 3
            else:
                stats[grupo][local]["pts"] += 1
                stats[grupo][visitante]["pts"] += 1

        for grupo, equipos_grupo in stats.items():
            for equipo, equipo_stats in equipos_grupo.items():
                equipo_stats["dg"] = equipo_stats["gf"] - equipo_stats["gc"]

    compute_stats()

    while True:
        zero_teams = [
            (grupo, equipo)
            for grupo, equipos_grupo in stats.items()
            for equipo, equipo_stats in equipos_grupo.items()
            if equipo_stats["pts"] == 0 or equipo_stats["gf"] == 0
        ]

        if not zero_teams:
            break

        changed = False
        for grupo, equipo in zero_teams:
            for match_data in matches_with_scores:
                if match_data["grupo"] != grupo:
                    continue

                if match_data["local"] == equipo and match_data["gl"] < match_data["gv"]:
                    match_data["gl"] = 1
                    match_data["gv"] = 1
                    changed = True
                    break
                if match_data["visitante"] == equipo and match_data["gv"] < match_data["gl"]:
                    match_data["gl"] = 1
                    match_data["gv"] = 1
                    changed = True
                    break
            if changed:
                break

        if not changed:
            break

        compute_stats()

    tabla_result = {}
    for grupo, equipos_grupo in stats.items():
        tabla_result[grupo] = dict(
            sorted(
                equipos_grupo.items(),
                key=lambda item: (item[1]["pts"], item[1]["dg"], item[1]["gf"]),
                reverse=True
            )
        )

    return tabla_result

def calcular_clasificacion():
    tabla = {}

    for grupo, equipos_lista in grupos.items():
        tabla[grupo] = {}

        for equipo in equipos_lista:
            tabla[grupo][equipo["name"]] = {
                "puntos": 0,
                "gf": 0,
                "gc": 0,
                "diferencia": 0
            }

    return tabla

# =========================
# INTENCIONES
# =========================

def detectar_intencion(p):
    if any(x in p for x in ["cuando juega", "cuándo juega", "partido", "fixture", "fecha"]):
        return "fixture"

    if any(x in p for x in ["clasifican", "clasifica", "clasificados", "clasificado"]):
        return "clasificacion"

    if any(x in p for x in ["ganara", "ganará", "quien gana", "quien ganara", "quien ganará", "quien sera", "quien será"]):
        return "prediccion"

    if any(x in p for x in ["mundiales", "mundial ha ganado", "copas del mundo", "copas mundiales", "campeon mundial"]):
        return "mundiales"

    if any(x in p for x in ["ranking", "fifa"]):
        return "ranking"

    if any(x in p for x in ["favorito", "favoritos", "favorita", "mejor equipo"]):
        return "favorito"

    if any(x in p for x in ["grupo"]):
        return "grupo"

    if any(x in p for x in ["cuantos equipos", "participantes", "equipos participantes"]):
        return "general"

    return "general"

def responder_chatbot(pregunta):
    p = normalizar(pregunta)
    intent = detectar_intencion(p)

    # =====================
    # CLASIFICACIÓN
    # =====================
    if intent == "clasificacion" or "clasifican" in p or "clasifica" in p:
        data = clasificados_por_grupo()
        for grupo, equipos_info in data.items():
            if normalizar(grupo) in p:
                return f"Clasificados del {grupo}: {equipos_info['1ro']} y {equipos_info['2do']}"
        return "Dime el grupo (A, B, C, D, E, F, G, H, I, J, K, L) para darte los clasificados."

    # =====================
    # PREDICCIÓN (¿QUIÉN GANARÁ GRUPO X?)
    # =====================
    if intent == "prediccion":
        for grupo in grupos:
            if normalizar(grupo) in p:
                ganador = obtener_ganador_grupo(grupo)
                return f"Según el ranking actual, el favorito para ganar {grupo} es {ganador}."
        if "mundial" in p or "campeon" in p:
            return "Los favoritos del Mundial son Argentina, Brasil y Francia."
        return "¿A qué grupo te refieres? (Grupo A, B, C, D, E, F, G, H, I, J, K, L)"

    # =====================
    # MUNDIALES GANADOS
    # =====================
    if intent == "mundiales":
        for equipo in equipos:
            if normalizar(equipo["name"]) in p:
                ganados = mundiales_ganados(equipo["name"])
                if ganados is not None:
                    return f"{equipo['name']} ha ganado {ganados} Copas del Mundo."
        return "¿A qué equipo te refieres? (ej: Brasil, Argentina, Alemania)"

    # =====================
    # FIXTURE (CUÁNDO JUEGA)
    # =====================
    if intent == "fixture":
        for match in matches:
            if normalizar(match["teamA"]) in p or normalizar(match["teamB"]) in p:
                location = match.get("location", "Sede Mundial 2026")
                return (
                    f"📅 El partido {match['teamA']} vs {match['teamB']} "
                    f"se jugará el {match['date']} en {location}."
                )
        return "¿A qué equipo o partido te refieres?"

    # =====================
    # RANKING FIFA
    # =====================
    if intent == "ranking":
        for equipo in equipos:
            if normalizar(equipo["name"]) in p:
                return f"{equipo['name']} está en el ranking FIFA #{equipo['ranking']}."
        return "¿A qué equipo te refieres?"

    # =====================
    # GRUPO
    # =====================
    if intent == "grupo":
        for equipo in equipos:
            if normalizar(equipo["name"]) in p:
                return f"{equipo['name']} pertenece al {equipo['group']}."
        return "¿A qué equipo te refieres?"

    # =====================
    # FAVORITO
    # =====================
    if intent == "favorito":
        return "Argentina, Brasil y Francia son los principales favoritos según el modelo."

    # =====================
    # BÚSQUEDA GENÉRICA DE EQUIPO
    # =====================
    for equipo in equipos:
        if normalizar(equipo["name"]) in p:
            return f"{equipo['name']} pertenece al {equipo['group']} y tiene ranking FIFA #{equipo['ranking']}."

    # =====================
    # GENERAL
    # =====================
    if "cuantos equipos" in p or "equipos participantes" in p or "equipos hay" in p:
        return "El Mundial 2026 tendrá 48 equipos participantes."

    if "accuracy" in p or "preciso" in p or "precision" in p or "f1" in p:
        return "El modelo tiene 58.4% accuracy y 55.1% F1-score."

    return (
        "🤖 No estoy seguro de eso todavía.\n\n"
        "Puedes preguntarme sobre:\n"
        "• ¿Quién ganará el Grupo A/B/C/...?\n"
        "• ¿Cuántos mundiales ha ganado Brasil?\n"
        "• ¿Cuál es el ranking de Argentina?\n"
        "• ¿Qué equipos clasifican del Grupo C?\n"
        "• ¿Cuándo juega Argentina?\n"
        "• ¿Quién es favorito?"
    )

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
    # Use DB-backed matches if available for richer predictions and filters
    db = 'mundial.db'
    q_group = request.args.get('group')
    q_team = request.args.get('team')
    min_prob = float(request.args.get('min_prob') or 0)

    matches_list = []
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'SELECT id, grupo, date, teamA, teamB, flagA, flagB, pred_probA, pred_probD, pred_probB, predicted, predicted_home_score, predicted_away_score, source FROM matches'
        clauses = []
        params = []
        if q_group:
            clauses.append('grupo = ?')
            params.append(q_group)
        if q_team:
            clauses.append('(teamA = ? OR teamB = ?)')
            params.extend([q_team, q_team])
        if clauses:
            sql += ' WHERE ' + ' AND '.join(clauses)
        cur.execute(sql, params)
        for row in cur.fetchall():
            mid, grupo, date, teamA, teamB, flagA, flagB, pA, pD, pB, predicted, ph, pa, source = row
            pA = pA or 0
            pD = pD or 0
            pB = pB or 0
            if max(pA, pD, pB) < min_prob:
                continue
            matches_list.append({
                'id': mid,
                'grupo': grupo,
                'date': date,
                'teamA': teamA,
                'teamB': teamB,
                'flagA': flagA,
                'flagB': flagB,
                'probWinA': round((pA or 0)*100,2),
                'probDraw': round((pD or 0)*100,2),
                'probWinB': round((pB or 0)*100,2),
                'predicted': predicted,
                'predicted_home_score': ph,
                'predicted_away_score': pa,
                'source': source,
            })
        conn.close()
    else:
        matches_list = matches

    groups_list = list(grupos.keys())
    return render_template("predicciones.html", matches=matches_list, flags=flags, groups=groups_list)

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/chatbot", methods=["GET"])
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/tabla")
def tabla():
    data = calcular_tabla_posiciones()
    return render_template("tabla.html", tabla=data)


@app.route("/estadisticas")
def estadisticas():
    db = 'mundial.db'
    stats = {}
    samples = []
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM teams")
        stats['teams'] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM matches")
        stats['matches'] = cur.fetchone()[0]
        cur.execute("SELECT source, COUNT(*) FROM matches GROUP BY source")
        stats['by_source'] = cur.fetchall()
        cur.execute("SELECT teamA, teamB, home_score, away_score, date, source FROM matches WHERE home_score IS NOT NULL OR away_score IS NOT NULL ORDER BY date DESC LIMIT 20")
        samples = cur.fetchall()
        conn.close()
    else:
        stats = {'teams': 0, 'matches': 0, 'by_source': []}

    return render_template('estadisticas.html', stats=stats, samples=samples)


@app.route('/export_csv')
def export_csv():
    db = 'mundial.db'
    si = io.StringIO()
    writer = csv.writer(si)
    header = ['id','grupo','date','teamA','teamB','home_score','away_score','predicted','pred_probA','pred_probD','pred_probB','source']
    writer.writerow(header)

    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        for row in cur.execute('SELECT id, grupo, date, teamA, teamB, home_score, away_score, predicted, pred_probA, pred_probD, pred_probB, source FROM matches'):
            writer.writerow(row)
        conn.close()

    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={"Content-disposition": "attachment; filename=matches_export.csv"})

# =========================
# API (TIEMPO REAL)
# =========================

@app.route("/api/chatbot", methods=["POST"])
def api_chatbot():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    respuesta = responder_chatbot(pregunta)

    return jsonify({"respuesta": respuesta})


@app.route('/api/matches', methods=['GET'])
def api_matches():
    db = 'mundial.db'
    out = []
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        q = "SELECT id, grupo, date, teamA, teamB, pred_probA, pred_probD, pred_probB, predicted, source FROM matches"
        for row in cur.execute(q):
            out.append({
                'id': row[0], 'grupo': row[1], 'date': row[2], 'teamA': row[3], 'teamB': row[4],
                'pred_probA': row[5], 'pred_probD': row[6], 'pred_probB': row[7], 'predicted': row[8], 'source': row[9]
            })
        conn.close()
    else:
        # fallback to in-memory
        for m in matches:
            out.append({
                'teamA': m.get('teamA'), 'teamB': m.get('teamB'), 'date': m.get('date'),
                'probWinA': m.get('probWinA'), 'probDraw': m.get('probDraw'), 'probWinB': m.get('probWinB')
            })
    return jsonify(out)

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)