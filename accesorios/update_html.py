"""
Actualiza docs/index.html:
1. Reemplaza bloque PLAYERS viejo con el nuevo
2. Actualiza CSS para mostrar datos bio
3. Actualiza template de tarjeta para mostrar nombre/club/dob/altura
4. Bump version a 2026.05.09.15
5. Actualiza CACHE_NAME
"""
import json, re, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

INDEX_PATH = r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\index.html'
PLAYERS_BLOCK_PATH = r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_block.js'

with open(INDEX_PATH, encoding='utf-8') as f:
    html = f.read()

with open(PLAYERS_BLOCK_PATH, encoding='utf-8') as f:
    new_players_raw = f.read()

# Indentar 4 espacios
new_players_indented = '\n'.join('    ' + l if l else '' for l in new_players_raw.split('\n'))

# ─── 1. Reemplazar bloque PLAYERS ───
old_start = html.find('    const PLAYERS = {')
# Buscar el cierre: '    };' que corresponde al PLAYERS
# Hay que encontrar el '};' en el nivel correcto
search_from = old_start + len('    const PLAYERS = {')
depth = 1
i = search_from
while i < len(html) and depth > 0:
    if html[i] == '{':
        depth += 1
    elif html[i] == '}':
        depth -= 1
    i += 1
# i ahora apunta justo después del último '}'
# Buscar el ';' que sigue
semi_pos = html.find(';', i - 1)
old_end = semi_pos + 1
old_block = html[old_start:old_end]
print(f'Bloque PLAYERS viejo: {len(old_block)} chars, líneas {html[:old_start].count(chr(10))+1}-{html[:old_end].count(chr(10))+1}')

html = html[:old_start] + new_players_indented + html[old_end:]
print('✓ PLAYERS actualizado')

# ─── 2. Actualizar CSS sticker-info ───
old_css = '''.sticker-info { padding: 5px 10px 3px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-grow: 1; gap: 1px; }
    .sticker-name { font-family: Montserrat, sans-serif; font-size: 0.72rem; font-weight: 900; color: #0a2a52; text-align: center; line-height: 1.2; }
    .sticker-role { font-family: Montserrat, sans-serif; font-size: 0.64rem; font-weight: 700; color: #4a5d7e; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }'''

new_css = '''.sticker-info { padding: 3px 6px 2px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-grow: 1; gap: 1px; overflow: hidden; }
    .sticker-name { font-family: Montserrat, sans-serif; font-size: 0.68rem; font-weight: 900; color: #0a2a52; text-align: center; line-height: 1.2; width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .sticker-bio { display: flex; flex-direction: column; align-items: center; gap: 0px; width: 100%; }
    .sticker-club { font-family: Montserrat, sans-serif; font-size: 0.58rem; font-weight: 700; color: #1a5fa8; text-align: center; width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .sticker-dob { font-family: Montserrat, sans-serif; font-size: 0.56rem; font-weight: 500; color: #6b7a8d; text-align: center; }
    .sticker-ht { font-family: Montserrat, sans-serif; font-size: 0.56rem; font-weight: 600; color: #3d6b9e; text-align: center; }
    .sticker-role { font-family: Montserrat, sans-serif; font-size: 0.60rem; font-weight: 700; color: #4a5d7e; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }'''

if old_css in html:
    html = html.replace(old_css, new_css)
    print('✓ CSS actualizado')
else:
    print('⚠ CSS no encontrado exactamente, buscando variante...')
    # Buscar por líneas individuales
    idx1 = html.find('.sticker-info { padding: 5px')
    if idx1 >= 0:
        idx_end = html.find('\n', html.find('.sticker-role {', idx1)) + 1
        html = html[:idx1] + new_css + html[idx_end:]
        print('✓ CSS actualizado (variante)')
    else:
        print('✗ CSS no actualizado - buscar manualmente')

# ─── 3. Actualizar template de tarjeta ───
old_template = """          const playerData = (PLAYERS[c] && PLAYERS[c][n]) ? PLAYERS[c][n] : null;
          const sName = playerData ? playerData[0] : "";
          const sRole = playerData ? playerData[1] : (()=>{
            if (n===1) return "Escudo";
            if (n<=3) return "Presentación";
            if (n===4||n===5) return "Arquero";
            if (n<=9) return "Defensa";
            if (n<=12) return "Mediocampista";
            return "Delantero";
          })();
          const flagInBand = FLAGS[c]
            ? `<img class="sticker-flag-img" src="${flagUrl(c, 80)}" alt="${c}" loading="lazy">`
            : `<span class="sticker-flag-emoji">${SPECIAL_EMOJI[c] || "⚽"}</span>`;
          card.innerHTML = `
            <div class="sticker-band">
              ${flagInBand}
              <div class="sticker-n">${n}</div>
            </div>
            <div class="sticker-mark">✓</div>
            <div class="sticker-info">
              ${sName ? `<div class="sticker-name">${sName}</div>` : ""}
              <div class="sticker-role">${sRole}</div>
            </div>"""

new_template = """          const pd = (PLAYERS[c] && PLAYERS[c][n]) ? PLAYERS[c][n] : null;
          const sName = pd ? pd.n : "";
          const sType = pd ? (pd.t || "J") : "J";
          const sRole = (() => {
            if (sType === "L") return "Escudo";
            if (sType === "F") return "Foto Equipo";
            return "";
          })();
          const sDob = pd && pd.d ? pd.d.split("-").reverse().join("/") : "";
          const sHt = pd && pd.h ? pd.h + " cm" : "";
          const sWt = pd && pd.w ? pd.w + " kg" : "";
          const sClub = pd && pd.c ? pd.c : "";
          const sPhys = sHt && sWt ? sHt + " · " + sWt : (sHt || sWt);
          const flagInBand = FLAGS[c]
            ? `<img class="sticker-flag-img" src="${flagUrl(c, 80)}" alt="${c}" loading="lazy">`
            : `<span class="sticker-flag-emoji">${SPECIAL_EMOJI[c] || "⚽"}</span>`;
          card.innerHTML = `
            <div class="sticker-band">
              ${flagInBand}
              <div class="sticker-n">${n}</div>
            </div>
            <div class="sticker-mark">✓</div>
            <div class="sticker-info">
              ${sName ? `<div class="sticker-name">${sName}</div>` : ""}
              ${sRole ? `<div class="sticker-role">${sRole}</div>` : ""}
              ${(sClub || sDob || sPhys) ? `<div class="sticker-bio">
                ${sClub ? `<div class="sticker-club">🏟 ${sClub}</div>` : ""}
                ${sDob ? `<div class="sticker-dob">🗓 ${sDob}</div>` : ""}
                ${sPhys ? `<div class="sticker-ht">📏 ${sPhys}</div>` : ""}
              </div>` : ""}
            </div>"""

if old_template in html:
    html = html.replace(old_template, new_template)
    print('✓ Template de tarjeta actualizado')
else:
    print('✗ Template de tarjeta no encontrado - verificar manualmente')
    # Mostrar contexto
    idx = html.find('const playerData')
    if idx >= 0:
        print('Encontrado en:', html[:idx].count('\n')+1)
        print(html[idx:idx+200])

# ─── 4. Bump versión ───
html = html.replace('const APP_VERSION = "2026.05.09.14"', 'const APP_VERSION = "2026.05.09.15"')
print('✓ APP_VERSION -> 2026.05.09.15')

# ─── 5. Bump CACHE_NAME en SW ───
# El SW está en sw.js, no en index.html. Solo actualizar version aquí.

# ─── Guardar ───
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\n✓ index.html guardado ({len(html)} chars)')

# Verificar
with open(INDEX_PATH, encoding='utf-8') as f:
    check = f.read()
print('APP_VERSION en HTML:', 'v15' in check.replace('2026.05.09.15', 'v15'))
print('PLAYERS en HTML:', 'const PLAYERS = {' in check)
print('sticker-club en HTML:', 'sticker-club' in check)
print('sClub en HTML:', 'sClub' in check)
