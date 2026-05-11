"""
Enriquece los datos de jugadores con: DOB, altura, peso, club
usando la API de Wikipedia en inglés.
Genera el CSV final y también el objeto JS PLAYERS listo para pegar en index.html.
"""

import json
import time
import re
import csv
from urllib.request import urlopen, Request
from urllib.parse import quote

HEADERS = {"User-Agent": "Mozilla/5.0 (FigusScraper/2.0; educational)"}

# Mapa de nombres que Wikipedia conoce diferente
NAME_FIXES = {
    "Emiliano Martinez": "Emiliano Martínez (footballer, born 1992)",
    "Nicolas Otamendi": "Nicolás Otamendi",
    "Nicolas Tagliafico": "Nicolás Tagliafico",
    "Lautaro Martinez": "Lautaro Martínez",
    "Julian Alvarez": "Julián Álvarez",
    "Giuliano Simeone": "Giuliano Simeone",
    "Franco Mastantuono": "Franco Mastantuono",
    "Nico Paz": "Nico Paz (footballer)",
    "Nico Gonzalez": "Nico González (footballer)",
    "Exequiel Palacios": "Exequiel Palacios",
    "Alexis Mac Allister": "Alexis Mac Allister",
    "Leonardo Balerdi": "Leonardo Balerdi",
    "Mohamed Salah": "Mohamed Salah",
    "Erling Haaland": "Erling Haaland",
    "Kylian Mbappe": "Kylian Mbappé",
    "Vinicius Junior": "Vinicius Júnior",
    "Vinicius Jr": "Vinicius Júnior",
    "Son Heung-min": "Son Heung-min",
    "Virgil van Dijk": "Virgil van Dijk",
    "Kevin De Bruyne": "Kevin De Bruyne",
}

# Datos manuales para jugadores difíciles de encontrar en Wikipedia
# formato: "Nombre Scanini": (dob, altura_cm, peso_kg, club)
MANUAL = {
    # FWC/historia
    "World Cup Trophy": ("—", "—", "—", "FIFA"),
    "FIFA": ("—", "—", "—", "FIFA"),
    # Jugadores poco conocidos o con nombres ambiguos
    "Giuliano Simeone": ("1999-07-07", "186", "78", "Atlético Madrid"),
    "Franco Mastantuono": ("2007-03-14", "180", "75", "Real Madrid"),
    "Nico Paz": ("2004-01-09", "177", "72", "Como"),
    "Nico Gonzalez": ("1997-12-06", "182", "79", "Barcelona"),
}

def wiki_extract(name):
    """Busca en Wikipedia y extrae DOB, altura, peso, club."""
    search_name = NAME_FIXES.get(name, name)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(search_name)}"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        extract = data.get("extract", "")
        return extract
    except:
        return ""


def parse_infobox(name):
    """Obtiene el HTML de la página y parsea el infobox para datos físicos."""
    search_name = NAME_FIXES.get(name, name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote(search_name)}&prop=revisions&rvprop=content&format=json&rvslots=main"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode())
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                return {}
            content = page.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("*", "")
            if not content:
                content = page.get("revisions", [{}])[0].get("*", "")
            return parse_wiki_content(content)
    except Exception as e:
        return {}


def parse_wiki_content(content):
    """Parsea el wikitext para extraer datos del infobox."""
    result = {}

    # DOB - birth_date
    m = re.search(r"\|\s*birth_date\s*=\s*.*?(\d{4})\|(\d{1,2})\|(\d{1,2})", content)
    if m:
        result["dob"] = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    else:
        # Otro formato: {{Birth date|1987|6|24}}
        m = re.search(r"[Bb]irth.date\|(\d{4})\|(\d{1,2})\|(\d{1,2})", content)
        if m:
            result["dob"] = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # Altura
    m = re.search(r"\|\s*height\s*=\s*\{\{convert\|(\d+(?:\.\d+)?)\|cm", content)
    if m:
        result["height"] = m.group(1)
    else:
        m = re.search(r"\|\s*height\s*=\s*(\d+(?:\.\d+)?)\s*(?:cm|m)?", content)
        if m:
            val = float(m.group(1))
            if val < 3:  # metros
                result["height"] = str(int(val * 100))
            else:
                result["height"] = str(int(val))

    # Peso
    m = re.search(r"\|\s*weight\s*=\s*\{\{convert\|(\d+)\|kg", content)
    if m:
        result["weight"] = m.group(1)
    else:
        m = re.search(r"\|\s*weight\s*=\s*(\d+)\s*(?:kg)?", content)
        if m:
            val = int(m.group(1))
            if 40 < val < 150:
                result["weight"] = str(val)

    # Club actual (currentclub o clubs con año vacío o —)
    m = re.search(r"\|\s*currentclub\s*=\s*([^\|\n\}]+)", content)
    if m:
        club = re.sub(r"\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]", r"\1", m.group(1)).strip()
        club = re.sub(r"\{\{.*?\}\}", "", club).strip()
        if club:
            result["club"] = club

    # Si no encontró club, buscar en clubs table el más reciente (año vacío = actual)
    if "club" not in result:
        # Buscar patrón "| | Club Name" (año vacío en tabla de clubs)
        clubs_section = re.findall(r"\|\s*\|\|\s*\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]", content)
        if clubs_section:
            result["club"] = clubs_section[-1]

    return result


def get_player_data(name):
    """Obtiene todos los datos de un jugador."""
    if name in MANUAL:
        m = MANUAL[name]
        return {"dob": m[0], "height": m[1], "weight": m[2], "club": m[3]}

    data = parse_infobox(name)
    time.sleep(0.3)
    return data


def main():
    # Cargar datos de Scanini
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.json", encoding="utf-8") as f:
        scanini = json.load(f)

    # Cargar CSV base
    rows_in = []
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows_in.append(row)

    # Obtener lista única de jugadores (evitar duplicados)
    players_seen = {}  # name -> {dob, height, weight, club}
    player_names = []
    for row in rows_in:
        if row["type"] == "player" and row["name"] not in players_seen:
            players_seen[row["name"]] = None
            player_names.append(row["name"])

    print(f"Total jugadores únicos: {len(player_names)}")

    # Buscar datos en Wikipedia (con caché)
    cache_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_cache.json"
    try:
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
    except:
        cache = {}

    total = len(player_names)
    for i, name in enumerate(player_names):
        if name in cache:
            continue
        print(f"  [{i+1}/{total}] {name}...", flush=True, end=" ")
        data = get_player_data(name)
        cache[name] = data
        result_str = f"DOB:{data.get('dob','?')} H:{data.get('height','?')} W:{data.get('weight','?')} Club:{data.get('club','?')}"
        print(result_str, flush=True)
        # Guardar caché cada 10 jugadores
        if i % 10 == 0:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)

    # Guardar caché final
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    print(f"\nCaché guardada con {len(cache)} jugadores")

    # Generar CSV final enriquecido
    rows_out = []
    for row in rows_in:
        name = row["name"]
        pdata = cache.get(name, {}) or {}
        rows_out.append({
            "team": row["team"],
            "num": row["num"],
            "name": name,
            "type": row["type"],
            "dob": pdata.get("dob", ""),
            "height": pdata.get("height", ""),
            "weight": pdata.get("weight", ""),
            "club": pdata.get("club", ""),
        })

    out_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_full.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["team","num","name","type","dob","height","weight","club"])
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"CSV final guardado: {out_path}")

    # Generar objeto JS PLAYERS
    players_js = {}
    for row in rows_out:
        t = row["team"]
        n = str(row["num"])
        if t not in players_js:
            players_js[t] = {}
        players_js[t][n] = {
            "name": row["name"],
            "type": row["type"],
            "dob": row["dob"],
            "height": row["height"],
            "weight": row["weight"],
            "club": row["club"],
        }

    js_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json"
    with open(js_path, "w", encoding="utf-8") as f:
        json.dump(players_js, f, ensure_ascii=False, indent=2)
    print(f"JSON JS guardado: {js_path}")


if __name__ == "__main__":
    main()
