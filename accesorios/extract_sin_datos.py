import re

with open('docs/index.html', encoding='utf-8') as f:
    html = f.read()

# Find the PLAYERS block
m = re.search(r'const PLAYERS\s*=\s*(\{.+?\});\s*\n', html, re.DOTALL)
if not m:
    print("NO ENCONTRE PLAYERS BLOCK")
    exit()

block = m.group(1)

# Find all country entries: "KEY":{entries}
country_pattern = re.compile(r'"([A-Z]+)"\s*:\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', re.DOTALL)

sin_datos = []

for cm in country_pattern.finditer(block):
    country = cm.group(1)
    players_str = cm.group(2)
    # Find individual player entries: number:{...}
    player_pattern = re.compile(r'(\d+)\s*:\s*\{([^}]+)\}')
    for pm in player_pattern.finditer(players_str):
        num = pm.group(1)
        data = pm.group(2)
        # Check if it's type J
        if 't:"J"' not in data and "t:'J'" not in data:
            continue
        # Check if it has NO data fields
        has_data = any(f in data for f in ['d:"', "d:'", 'h:', 'c:"', "c:'"])
        if not has_data:
            # Extract name
            nm = re.search(r'n:"([^"]+)"', data)
            if not nm:
                nm = re.search(r"n:'([^']+)'", data)
            name = nm.group(1) if nm else "???"
            sin_datos.append((country, int(num), name))

sin_datos.sort(key=lambda x: (x[0], x[1]))

# Separate FWC special stickers from real players
NO_SON_JUGADORES = ['Official Emblem', 'Official Mascots', 'Official Slogan', 'Official Ball',
                    'Host Countries', 'World Cup History']

jugadores = [(c, n, name) for c, n, name in sin_datos
             if not any(tag in name for tag in NO_SON_JUGADORES)]
especiales = [(c, n, name) for c, n, name in sin_datos
              if any(tag in name for tag in NO_SON_JUGADORES)]

print(f"Total sin datos: {len(sin_datos)}")
print(f"  -> Jugadores reales sin datos: {len(jugadores)}")
print(f"  -> Especiales FWC (no son jugadores): {len(especiales)}")
print()

lines_j = [f"{c}|{n}|{name}" for c, n, name in jugadores]
lines_e = [f"{c}|{n}|{name}" for c, n, name in especiales]

# Save full list (all)
with open('jugadores_sin_datos.txt', 'w', encoding='utf-8') as f:
    f.write("=== JUGADORES REALES SIN DATOS (" + str(len(jugadores)) + ") ===\n")
    f.write('\n'.join(lines_j))
    f.write("\n\n=== ESPECIALES FWC (no son jugadores, no pedir datos) ===\n")
    f.write('\n'.join(lines_e))
    f.write('\n')

# Save prompt (only real players)
prompt = """Tengo un álbum de figuritas del Mundial 2026. Necesito que busques los datos de los siguientes jugadores de fútbol.

Para cada jugador necesito exactamente estos 4 datos (vigentes al 11 de mayo de 2026):
- Fecha de nacimiento (formato YYYY-MM-DD)
- Altura en centímetros (solo el número entero)
- Club actual (nombre real del club, sin corchetes ni wikisyntax)
- Posición en español: Portero / Defensa / Centrocampista / Delantero

FORMATO DE RESPUESTA — una línea por jugador, EXACTAMENTE así, sin encabezados ni explicaciones:
PAIS|NUM|NOMBRE|YYYY-MM-DD|altura_cm|Club Actual|Posicion

Reglas:
- Si no encontrás un dato específico, poné ? en ese campo.
- NO omitas ningún jugador de la lista.
- No agregues texto extra, solo las líneas con los datos.
- Los nombres de clubes van en su idioma original (ej: "Manchester City", "Real Madrid", "Bayern München").

LISTA DE JUGADORES (""" + str(len(jugadores)) + """ jugadores):
PAIS|NUM|NOMBRE
""" + '\n'.join(lines_j) + """

Respuesta esperada: """ + str(len(jugadores)) + """ líneas, una por jugador, formato PAIS|NUM|NOMBRE|YYYY-MM-DD|altura_cm|Club|Posicion
"""

with open('prompt_para_ia.txt', 'w', encoding='utf-8') as f:
    f.write(prompt)

print("Archivos guardados:")
print("  jugadores_sin_datos.txt  (lista completa)")
print("  prompt_para_ia.txt       (prompt listo para otra IA)")
print()
print("=== JUGADORES REALES SIN DATOS ===")
for c, n, name in jugadores:
    print(f"  {c}|{n}|{name}")
print()
print("=== FWC ESPECIALES (no incluidos en el prompt) ===")
for c, n, name in especiales:
    print(f"  {c}|{n}|{name}")
