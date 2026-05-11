"""
Genera el bloque PLAYERS para index.html a partir de players_data.json.
Ejecutar DESPUÉS de que enrich_players2.py termine.
"""

import json, re, sys

# Mapeo de teams de la app (algunos difieren del JSON de Scanini)
# COW en la app = CIV en Scanini (Costa de Marfil)
# CUW en Scanini NO está en la app -> se ignora
TEAM_MAP = {
    "CIV": "COW",  # Scanini CIV -> app COW (Costa de Marfil)
}
SKIP_TEAMS = {"CUW"}  # Curaçao no está en la app

# Posiciones genéricas según el nombre del sticker type de Scanini
TYPE_TO_ESP = {
    "player": "Jugador",
    "team logo · foil": "Logo",
    "team logo": "Logo",
    "team photo": "Foto Equipo",
    "foil": "Foil",
    "special": "Especial",
    "badge": "Escudo",
}

def fmt_dob(dob_str):
    """Convierte 1987-06-24 -> 24/06/1987"""
    if not dob_str or dob_str == "?":
        return ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", dob_str)
    if m:
        return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
    return ""

def clean_club(club):
    """Limpia el nombre del club."""
    if not club or club == "?":
        return ""
    # Quitar prefijos como [[Club Name (no link)
    club = re.sub(r"^\[\[", "", club)
    # Quitar sufijos tipo " F.C.", " FC" duplicados etc.
    club = club.strip()
    return club

def js_str(s):
    """Escapa string para JS."""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")

def main():
    # Cargar datos enriquecidos
    try:
        with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json", encoding="utf-8") as f:
            players_data = json.load(f)
    except FileNotFoundError:
        print("ERROR: players_data.json no encontrado. Corre primero enrich_players2.py")
        sys.exit(1)

    print(f"Equipos en players_data.json: {list(players_data.keys())}")

    lines = ["const PLAYERS = {"]

    # Procesar en orden
    for team, stickers in sorted(players_data.items()):
        if team in SKIP_TEAMS:
            continue

        # Mapear nombre de equipo para la app
        app_team = TEAM_MAP.get(team, team)

        lines.append(f'  "{app_team}": {{')

        for num_str, data in sorted(stickers.items(), key=lambda x: int(x[0])):
            name = js_str(data.get("name", ""))
            stype = data.get("type", "player")
            dob = fmt_dob(data.get("dob", ""))
            height = data.get("height", "") or ""
            weight = data.get("weight", "") or ""
            club = js_str(clean_club(data.get("club", "")))

            # Tipo legible
            type_label = TYPE_TO_ESP.get(stype.lower(), "Jugador")
            # Para figuras especiales sin datos, solo mostrar nombre y tipo
            entry = f'    {num_str}: {{name:"{name}",type:"{type_label}"'
            if dob:
                entry += f',dob:"{dob}"'
            if height:
                entry += f',height:"{height}"'
            if weight:
                entry += f',weight:"{weight}"'
            if club:
                entry += f',club:"{club}"'
            entry += "},"
            lines.append(entry)

        lines.append("  },")

    lines.append("};")

    output = "\n".join(lines)

    # Guardar el bloque JS
    out_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_block.js"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Bloque JS guardado en: {out_path}")
    print(f"Líneas: {len(lines)}")

    # Estadísticas
    total = 0
    with_name = 0
    with_dob = 0
    with_height = 0
    with_club = 0
    for team, stickers in players_data.items():
        for num, data in stickers.items():
            total += 1
            if data.get("name"): with_name += 1
            if data.get("dob"): with_dob += 1
            if data.get("height"): with_height += 1
            if data.get("club"): with_club += 1
    print(f"\nEstadísticas:")
    print(f"  Total stickers: {total}")
    print(f"  Con nombre: {with_name}")
    print(f"  Con DOB: {with_dob}")
    print(f"  Con altura: {with_height}")
    print(f"  Con club: {with_club}")

if __name__ == "__main__":
    main()
