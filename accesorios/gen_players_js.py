"""Genera el bloque PLAYERS compacto para index.html"""
import json

with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json", encoding="utf-8") as f:
    data = json.load(f)

TYPE_MAP = {
    "player": "J",
    "team logo": "L", "team logo foil": "L", "team logo . foil": "L",
    "team logo · foil": "L", "team logo- foil": "L",
    "team photo": "F",
}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

lines = ["const PLAYERS = {"]
for team, stickers in sorted(data.items()):
    lines.append(f'  "{team}":'  + "{")
    for num, info in sorted(stickers.items(), key=lambda x: int(x[0])):
        nm = esc(info.get("name", ""))
        tp = info.get("type", "player").lower().strip()
        # Simplify type key
        tp_clean = tp.replace(" · foil", "").replace("foil", "").strip()
        t = TYPE_MAP.get(tp_clean, "J")
        parts = [f'n:"{nm}"', f't:"{t}"']
        if info.get("dob"):    parts.append(f'd:"{info["dob"]}"')
        if info.get("height"): parts.append(f'h:"{info["height"]}"')
        if info.get("weight"): parts.append(f'w:"{info["weight"]}"')
        if info.get("club"):   parts.append(f'c:"{esc(info["club"])}"')
        lines.append(f'    {num}:' + "{" + ",".join(parts) + "},")
    lines.append("  },")
lines.append("};")

output = "\n".join(lines)
out = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_block.js"
with open(out, "w", encoding="utf-8") as f:
    f.write(output)
print(f"Guardado {len(lines)} lineas en {out}")
# Muestra ARG
print("\nARG muestra:")
for n in range(1, 21):
    e = data.get("ARG", {}).get(str(n), {})
    print(f"  {n:2d}: {e.get('name','?')} | {e.get('club','')} | {e.get('dob','')}")
