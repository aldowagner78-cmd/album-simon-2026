"""
Script definitivo: obtiene datos de jugadores via Wikidata API (datos estructurados).
Wikidata tiene DOB, altura, peso y club actual en formato limpio.
"""

import json, time, re, csv, sys
from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

HEADERS = {"User-Agent": "Mozilla/5.0 (FigusScraper/3.0; educational)"}

# Nombres exactos de Wikipedia en inglés para búsqueda en Wikidata
NAME_WIKI = {
    # Argelia
    "Alexis Guendouz": "Alexis Guendouz",
    "Ramy Bensebaini": "Ramy Bensebaini",
    "Youcef Atal": "Youcef Atal",
    "Rayan Aït-Nouri": "Rayan Aït-Nouri",
    "Mohamed Amine Tougai": "Mohamed Amine Tougaï",
    "Aïssa Mandi": "Aïssa Mandi",
    "Ismael Bennacer": "Ismaël Bennacer",
    "Houssem Aquar": "Houssem Aouar",
    "Hicham Boudaoui": "Hicham Boudaoui",
    "Ramiz Zerrouki": "Ramiz Zerrouki",
    "Nabil Bentalab": "Nabil Bentaleb",
    "Fares Chaibi": "Farès Chaibi",
    "Riyad Mahrez": "Riyad Mahrez",
    "Said Benrahma": "Saïd Benrahma",
    "Anis Hadj Moussa": "Anis Hadj Moussa",
    "Amine Gouiri": "Amine Gouiri",
    "Baghdad Bounedjah": "Baghdad Bounedjah",
    "Mohammed Amoura": "Mohamed Amoura",
    # Argentina
    "Emiliano Martinez": "Emiliano Martínez (footballer, born 1992)",
    "Nahuel Molina": "Nahuel Molina",
    "Cristian Romero": "Cristián Romero",
    "Nicolas Otamendi": "Nicolás Otamendi",
    "Nicolas Tagliafico": "Nicolás Tagliafico",
    "Leonardo Balerdi": "Leonardo Balerdi",
    "Enzo Fernandez": "Enzo Fernández",
    "Alexis Mac Allister": "Alexis Mac Allister",
    "Rodrigo De Paul": "Rodrigo De Paul",
    "Exequiel Palacios": "Exequiel Palacios",
    "Leandro Paredes": "Leandro Paredes",
    "Franco Mastantuono": "Franco Mastantuono",
    "Nico Paz": "Nico Paz (footballer)",
    "Nico Gonzalez": "Nico González (footballer)",
    "Lionel Messi": "Lionel Messi",
    "Lautaro Martinez": "Lautaro Martínez",
    "Julian Alvarez": "Julián Álvarez",
    "Giuliano Simeone": "Giuliano Simeone",
    # Brasil
    "Alisson": "Alisson Becker",
    "Bento": "Bento (footballer, born 1999)",
    "Marquinhos": "Marquinhos (footballer)",
    "Éder Militão": "Éder Militão",
    "Gabriel Magalhães": "Gabriel Magalhães",
    "Danilo": "Danilo (Brazilian footballer)",
    "Wesley": "Wesley (Brazilian footballer, born 2003)",
    "Lucas Paquetá": "Lucas Paquetá",
    "Casemiro": "Casemiro",
    "Bruno Guimarães": "Bruno Guimarães",
    "Luiz Henrique": "Luiz Henrique (Brazilian footballer, born 2001)",
    "Vinicius Júnior": "Vinicius Júnior",
    "Rodrygo": "Rodrygo",
    "João Pedro": "João Pedro (footballer, born 2001)",
    "Matheus Cunha": "Matheus Cunha",
    "Gabriel Martinelli": "Gabriel Martinelli",
    "Raphinha": "Raphinha",
    "Estévão": "Estêvão Willian",
    # Australia
    "Mathew Ryan": "Mathew Ryan",
    "Joe Gauci": "Joe Gauci",
    "Harry Souttar": "Harry Souttar",
    "Alessandro Circati": "Alessandro Circati",
    "Jordan Bos": "Jordan Bos",
    "Aziz Behich": "Aziz Behich",
    "Cameron Burgess": "Cameron Burgess",
    "Lewis Miller": "Lewis Miller (footballer)",
    "Milos Degenek": "Miloš Degenek",
    "Jackson Irvine": "Jackson Irvine",
    "Riley McGree": "Riley McGree",
    "Aiden O'Neill": "Aiden O'Neill (footballer)",
    "Connor Metcalfe": "Connor Metcalfe",
    "Patrick Yazbek": "Patrick Yazbek",
    "Craig Goodwin": "Craig Goodwin",
    "Kusini Vengi": "Kusini Yengi",
    "Nestory Irankunda": "Nestory Irankunda",
    "Mohamed Touré": "Mohamed Touré (Australian footballer)",
    # Austria
    "Alexander Schlager": "Alexander Schlager",
    "Patrick Pentz": "Patrick Pentz",
    "David Alaba": "David Alaba",
    "Kevin Danso": "Kevin Danso",
    "Philipp Lienhart": "Philipp Lienhart",
    "Stefan Posch": "Stefan Posch",
    "Phillipp Mwene": "Phillipp Mwene",
    "Alexander Prass": "Alexander Prass",
    "Xaver Schlager": "Xaver Schlager",
    "Marcel Sabitzer": "Marcel Sabitzer",
    "Konrad Laimer": "Konrad Laimer",
    "Florian Grillitsch": "Florian Grillitsch",
    "Nicolas Seiwald": "Nicolas Seiwald",
    "Romano Schmid": "Romano Schmid",
    "Patrick Wimmer": "Patrick Wimmer",
    "Christoph Baumgartner": "Christoph Baumgartner",
    "Michael Gregoritsch": "Michael Gregoritsch",
    "Marko Arnautović": "Marko Arnautović",
    # Bélgica
    "Thibaut Courtois": "Thibaut Courtois",
    "Arthur Theate": "Arthur Theate",
    "Timothy Castagne": "Timothy Castagne",
    "Zeno Debast": "Zeno Debast",
    "Brandon Mechele": "Brandon Mechele",
    "Maxim De Cuyper": "Maxim De Cuyper",
    "Thomas Meunier": "Thomas Meunier",
    "Youri Tielemans": "Youri Tielemans",
    "Amadou Onana": "Amadou Onana",
    "Nicolas Raskin": "Nicolas Raskin",
    "Alexis Saelemaekers": "Alexis Saelemaekers",
    "Hans Vanaken": "Hans Vanaken",
    "Kevin De Bruyne": "Kevin De Bruyne",
    "Jérémy Doku": "Jérémy Doku",
    "Charles De Ketelaere": "Charles De Ketelaere",
    "Leandro Trossard": "Leandro Trossard",
    "Loïs Openda": "Loïs Openda",
    "Romelu Lukaku": "Romelu Lukaku",
}


def wikidata_search(name):
    """Busca en Wikidata por nombre y obtiene datos del jugador."""
    # Usar la API de búsqueda de Wikidata
    params = urlencode({
        "action": "wbsearchentities",
        "search": name,
        "language": "en",
        "type": "item",
        "format": "json",
        "limit": 3
    })
    url = f"https://www.wikidata.org/w/api.php?{params}"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        results = data.get("search", [])
        # Buscar el primero que sea un jugador de fútbol
        for result in results:
            desc = result.get("description", "").lower()
            if any(word in desc for word in ["football", "soccer", "footballer"]):
                return result.get("id")
        # Si no hay descripción de fútbol, tomar el primero
        if results:
            return results[0].get("id")
    except:
        pass
    return None


def wikidata_get_entity(qid):
    """Obtiene los datos de una entidad de Wikidata."""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json&languages=en&props=claims|labels"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode())
        entity = data.get("entities", {}).get(qid, {})
        claims = entity.get("claims", {})
        result = {}

        # P569 = date of birth
        dob_claims = claims.get("P569", [])
        if dob_claims:
            dob_val = dob_claims[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if isinstance(dob_val, dict):
                time_str = dob_val.get("time", "")
                m = re.search(r"\+(\d{4})-(\d{2})-(\d{2})", time_str)
                if m:
                    result["dob"] = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

        # P2048 = height (cm)
        height_claims = claims.get("P2048", [])
        if height_claims:
            h_val = height_claims[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if isinstance(h_val, dict):
                amount = h_val.get("amount", "")
                unit = h_val.get("unit", "")
                if "centimetre" in unit or "Q174728" in unit:
                    result["height"] = str(int(float(amount.replace("+", ""))))
                elif "metre" in unit or "Q11573" in unit:
                    result["height"] = str(int(float(amount.replace("+", "")) * 100))
                elif amount:
                    val = float(amount.replace("+", ""))
                    if val > 100:
                        result["height"] = str(int(val))
                    elif val > 1:
                        result["height"] = str(int(val * 100))

        # P2067 = mass/weight (kg)
        weight_claims = claims.get("P2067", [])
        if weight_claims:
            w_val = weight_claims[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if isinstance(w_val, dict):
                amount = w_val.get("amount", "")
                if amount:
                    val = float(amount.replace("+", ""))
                    if 40 < val < 150:
                        result["weight"] = str(int(val))

        # P54 = member of sports team (buscar sin fecha final = actual)
        team_claims = claims.get("P54", [])
        current_club = None
        for claim in team_claims:
            qualifiers = claim.get("qualifiers", {})
            end_time = qualifiers.get("P582", [])  # end time
            if not end_time:  # sin fecha final = club actual
                team_id = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
                if team_id:
                    # Obtener nombre del equipo
                    club_name = get_entity_label(team_id)
                    if club_name:
                        current_club = club_name
                        break
        if current_club:
            result["club"] = current_club

        # P413 = position
        pos_claims = claims.get("P413", [])
        if pos_claims:
            pos_id = pos_claims[0].get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
            if pos_id:
                pos_map = {
                    "Q182574": "Mediocampista", "Q189571": "Delantero",
                    "Q200768": "Defensa", "Q208485": "Extremo",
                    "Q216723": "Arquero", "Q1080706": "Defensa Central",
                    "Q1815485": "Lateral", "Q2234021": "Volante",
                    "Q2716932": "Mediocampista Central", "Q204832": "Delantero Centro",
                }
                result["position"] = pos_map.get(pos_id, "")

        return result
    except Exception as e:
        return {}


def get_entity_label(qid):
    """Obtiene el nombre de una entidad de Wikidata."""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json&languages=en&props=labels"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        labels = data.get("entities", {}).get(qid, {}).get("labels", {})
        return labels.get("en", {}).get("value", "")
    except:
        return ""


# Cache de QIDs para evitar búsquedas repetidas
qid_cache = {}

def get_player_data(name):
    """Pipeline completo: buscar QID → obtener datos."""
    wiki_name = NAME_WIKI.get(name, name)

    # Buscar QID
    if wiki_name not in qid_cache:
        qid = wikidata_search(wiki_name)
        qid_cache[wiki_name] = qid
        time.sleep(0.2)
    else:
        qid = qid_cache[wiki_name]

    if not qid:
        return {}

    data = wikidata_get_entity(qid)
    time.sleep(0.2)
    return data


def main():
    # Limpiar caché vieja (quitar entradas vacías para re-procesar)
    cache_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_cache.json"
    try:
        with open(cache_path, encoding="utf-8") as f:
            old_cache = json.load(f)
    except:
        old_cache = {}

    # Solo conservar entradas con datos reales
    cache = {k: v for k, v in old_cache.items() if v and (v.get("dob") or v.get("height") or v.get("club"))}
    print(f"Caché limpiada: {len(old_cache)} → {len(cache)} entradas con datos reales")

    # Cargar lista de jugadores
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.csv", encoding="utf-8") as f:
        rows_in = list(csv.DictReader(f))

    player_names = []
    seen = set()
    for row in rows_in:
        n = row["name"]
        if row["type"] == "player" and n not in seen:
            seen.add(n)
            player_names.append(n)

    total = len(player_names)
    already = sum(1 for p in player_names if p in cache)
    print(f"Total jugadores: {total} | Ya en caché: {already} | Por buscar: {total - already}")

    for i, name in enumerate(player_names):
        if name in cache:
            continue
        print(f"[{i+1}/{total}] {name}... ", end="", flush=True)
        data = get_player_data(name)
        cache[name] = data
        dob = data.get('dob', '?')
        h = data.get('height', '?')
        w = data.get('weight', '?')
        club = data.get('club', '?')[:20] if data.get('club') else '?'
        print(f"DOB:{dob} H:{h} W:{w} Club:{club}", flush=True)

        if (i + 1) % 30 == 0:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            print(f"  [caché guardada: {len(cache)} entradas]")

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    # Estadísticas finales
    with_dob = sum(1 for v in cache.values() if v and v.get('dob'))
    with_h = sum(1 for v in cache.values() if v and v.get('height'))
    with_club = sum(1 for v in cache.values() if v and v.get('club'))
    print(f"\nEstadísticas: DOB:{with_dob} Altura:{with_h} Club:{with_club} / {total} total")

    # Generar CSV y JSON finales
    rows_out = []
    for row in rows_in:
        pdata = cache.get(row["name"], {}) or {}
        rows_out.append({
            "team": row["team"], "num": row["num"],
            "name": row["name"], "type": row["type"],
            "dob": pdata.get("dob", ""), "height": pdata.get("height", ""),
            "weight": pdata.get("weight", ""), "club": pdata.get("club", ""),
            "position": pdata.get("position", ""),
        })

    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_full.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["team","num","name","type","dob","height","weight","club","position"])
        w.writeheader(); w.writerows(rows_out)
    print("CSV guardado: stickers_full.csv")

    by_team = {}
    for row in rows_out:
        t, n = row["team"], row["num"]
        if t not in by_team:
            by_team[t] = {}
        by_team[t][n] = {k: row[k] for k in ["name","type","dob","height","weight","club","position"]}

    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json", "w", encoding="utf-8") as f:
        json.dump(by_team, f, ensure_ascii=False, indent=2)
    print("JSON guardado: players_data.json")

if __name__ == "__main__":
    main()
