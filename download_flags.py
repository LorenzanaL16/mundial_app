import os
import requests

CARPETA = "static/img/flags"
os.makedirs(CARPETA, exist_ok=True)

paises = {
    "mexico": "mx",
    "sudafrica": "za",
    "corea-del-sur": "kr",
    "republica-checa": "cz",

    "canada": "ca",
    "bosnia-y-herzegovina": "ba",
    "qatar": "qa",
    "suiza": "ch",

    "brasil": "br",
    "marruecos": "ma",
    "haiti": "ht",
    "escocia": "gb-sct",

    "estados-unidos": "us",
    "paraguay": "py",
    "australia": "au",
    "turquia": "tr",

    "alemania": "de",
    "curazao": "cw",
    "costa-de-marfil": "ci",
    "ecuador": "ec",

    "paises-bajos": "nl",
    "japon": "jp",
    "suecia": "se",
    "tunez": "tn",

    "belgica": "be",
    "egipto": "eg",
    "iran": "ir",
    "nueva-zelanda": "nz",

    "espana": "es",
    "cabo-verde": "cv",
    "arabia-saudita": "sa",
    "uruguay": "uy",

    "francia": "fr",
    "senegal": "sn",
    "irak": "iq",
    "noruega": "no",

    "argentina": "ar",
    "argelia": "dz",
    "austria": "at",
    "jordania": "jo",

    "portugal": "pt",
    "rd-congo": "cd",
    "uzbekistan": "uz",
    "colombia": "co",

    "inglaterra": "gb-eng",
    "croacia": "hr",
    "ghana": "gh",
    "panama": "pa",
}

for nombre, codigo in paises.items():
    ruta = os.path.join(CARPETA, f"{nombre}.png")

    if os.path.exists(ruta):
        print(f"✔ Ya existe: {nombre}")
        continue

    url = f"https://flagcdn.com/w80/{codigo}.png"

    print(f"Descargando {nombre}...")

    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        with open(ruta, "wb") as f:
            f.write(r.content)
        print("✔ Guardado")
    else:
        print("❌ Error:", nombre)

        