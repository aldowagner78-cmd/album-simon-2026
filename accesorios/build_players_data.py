"""
Genera players_data.json a partir del cache actual (parcial) + stickers_scanini.json.
Permite desplegar el álbum con datos parciales mientras el enriquecimiento sigue.
"""

import json, re, sys

def clean_club(club):
    if not club:
        return ""
    # Limpiar wikilinks: [[Club|Display]] -> Display, [[Club]] -> Club
    club = re.sub(r"\[\[([^\|\]]+)\|([^\]]+)\]\]", r"\2", club)  # [[A|B]] -> B
    club = re.sub(r"\[\[([^\|\]]+)\]\]", r"\1", club)            # [[A]] -> A
    # Quitar cualquier bracket restante
    club = re.sub(r"\[+|\]+", "", club)
    club = re.sub(r"\{\{[^}]*\}\}", "", club)
    club = re.sub(r"<!--.*?-->", "", club)
    club = re.sub(r"\s*\(on loan.*?\)", "", club, flags=re.IGNORECASE)
    club = re.sub(r"\s+", " ", club).strip()
    return club

def fmt_dob(dob_str):
    """1987-06-24 -> 24/06/1987"""
    if not dob_str:
        return ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", dob_str)
    if m:
        return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
    return ""

# Mapeo: Scanini team code -> app team code
TEAM_MAP = {
    "CIV": "COW",  # Costa de Marfil -> el código de la app
}
SKIP_TEAMS = {"CUW"}  # Curaçao no está en la app

# Cargar stickers de Scanini (fuente de verdad para orden + nombres)
with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.json", encoding="utf-8") as f:
    scanini = json.load(f)

print(f"Stickers Scanini: {sum(len(v) for v in scanini.values())} en {len(scanini)} equipos")

# Cargar caché de enriquecimiento
try:
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_cache.json", encoding="utf-8") as f:
        cache = json.load(f)
    print(f"Cache: {len(cache)} jugadores enriquecidos")
except:
    cache = {}
    print("Cache vacío")

# Construir players_data.json
by_team = {}
total = 0
enriched = 0

for scanini_team, stickers in sorted(scanini.items()):
    if scanini_team in SKIP_TEAMS:
        continue

    app_team = TEAM_MAP.get(scanini_team, scanini_team)
    by_team[app_team] = {}

    for num_str, sdata in sorted(stickers.items(), key=lambda x: int(x[0])):
        total += 1
        name = sdata.get("name", "")
        stype = sdata.get("type", "player")

        # Buscar datos de enriquecimiento
        pdata = cache.get(name, {}) or {}
        dob = fmt_dob(pdata.get("dob", ""))
        height = pdata.get("height", "") or ""
        weight = pdata.get("weight", "") or ""
        club = clean_club(pdata.get("club", ""))

        if dob or height or club:
            enriched += 1

        entry = {
            "name": name,
            "type": stype,
        }
        if dob: entry["dob"] = dob
        if height: entry["height"] = height
        if weight: entry["weight"] = weight
        if club: entry["club"] = club

        by_team[app_team][num_str] = entry

print(f"Total stickers procesados: {total}")
print(f"Con datos bio: {enriched} ({enriched*100//total}%)")

# También duplicar COW = CIV (la app tiene ambos?)
# De hecho, en el COUNTRIES de la app solo está COW (no CIV)
# El mapeo arriba ya lo resuelve.

# Guardar JSON
out_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(by_team, f, ensure_ascii=False, indent=2)
print(f"players_data.json guardado: {len(by_team)} equipos")

# Verificar ARG
print("\n=== ARG primeros 20 ===")
for n in range(1, 21):
    e = by_team.get("ARG", {}).get(str(n), {})
    print(f"  {n:2d}: {e.get('name','?')} | {e.get('club','')} | {e.get('dob','')}")
