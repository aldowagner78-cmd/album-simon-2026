"""
Extrae escudos faltantes de escudos_fuente.JPG y normaliza
TODOS los escudos a 200x200 px, fondo blanco, misma apariencia.

Layout de escudos_fuente.JPG (502x357):
 - 2 mitades horizontales: izq (x 0-251) y der (x 251-502)
 - 6 filas por mitad, cada fila ~59.5px
 - Cada fila: título ~13px arriba, 4 escudos iguales debajo
 - 4 columnas por mitad, ~62.75px cada una

Mapa:
 Izq  A: MEX RSA KOR CZE
 Izq  B: CAN BIH QAT SUI
 Izq  C: BRA MAR HAI SCO
 Izq  D: USA PAR AUS TUR
 Izq  E: GER COW CIV ECU
 Izq  F: NED JPN SWE TUN
 Der  G: BEL EGY IRN NZL
 Der  H: ESP CPV KSA URU
 Der  I: FRA SEN IRQ NOR
 Der  J: ARG ALG AUT JOR
 Der  K: POR COD UZB COL
 Der  L: ENG CRO GHA PAN
"""
import os
from PIL import Image

SRC  = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\escudos_fuente.JPG"
OUT  = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\img\stickers"
SIZE = 200   # tamaño final uniforme
PAD  = 12    # padding interno en el cuadrado final

img = Image.open(SRC)
W, H = img.size   # 502, 357

half_w   = W / 2        # 251
row_h    = H / 6        # 59.5
title_h  = 13           # px que ocupa el título de grupo
col_w    = half_w / 4   # 62.75

def crop_shield(side, row, col):
    """
    side: 'L' (izquierda) o 'R' (derecha)
    row:  0-5
    col:  0-3
    Devuelve imagen recortada del escudo.
    """
    x0 = (0 if side == 'L' else half_w) + col * col_w + 2
    x1 = x0 + col_w - 4
    y0 = row * row_h + title_h + 1
    y1 = (row + 1) * row_h - 2
    return img.crop((int(x0), int(y0), int(x1), int(y1)))

def to_square_white(shield_img, size=SIZE, pad=PAD):
    """Pone el escudo en un cuadrado blanco uniforme."""
    shield_img = shield_img.convert("RGBA")
    shield_img.thumbnail((size - pad*2, size - pad*2), Image.LANCZOS)
    bg = Image.new("RGB", (size, size), (255, 255, 255))
    sw, sh = shield_img.size
    ox = (size - sw) // 2
    oy = (size - sh) // 2
    bg.paste(shield_img, (ox, oy), shield_img.split()[3])
    return bg

# Escudos a extraer de la imagen fuente
# (código, side, row, col)
EXTRACT = [
    ("BIH", 'L', 1, 1),
    ("HAI", 'L', 2, 2),
    ("PAR", 'L', 3, 1),
    ("TUR", 'L', 3, 3),
    ("COW", 'L', 4, 1),
    ("ECU", 'L', 4, 3),
    ("NZL", 'R', 0, 3),
    ("AUT", 'R', 3, 2),
    ("PAN", 'R', 5, 3),
]

print("=== Extrayendo escudos faltantes ===")
for code, side, row, col in EXTRACT:
    out_path = os.path.join(OUT, f"{code}-1.jpg")
    shield = crop_shield(side, row, col)
    final  = to_square_white(shield)
    final.save(out_path, "JPEG", quality=95)
    print(f"  ✅ {code}-1.jpg guardado ({shield.size[0]}x{shield.size[1]} → {SIZE}x{SIZE})")

# Para CC (CONCACAF) - no está en la imagen, usar fondo blanco con texto
from PIL import ImageDraw, ImageFont
cc_path = os.path.join(OUT, "CC-1.jpg")
cc_img = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
draw = ImageDraw.Draw(cc_img)
draw.ellipse([20, 20, 180, 180], outline=(0, 80, 160), width=8)
draw.text((SIZE//2, SIZE//2), "CONCACAF", fill=(0, 80, 160), anchor="mm")
cc_img.save(cc_path, "JPEG", quality=95)
print("  ✅ CC-1.jpg (placeholder)")

# FWC si no existe
fwc_path = os.path.join(OUT, "FWC-1.jpg")
if not os.path.exists(fwc_path):
    fwc_img = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(fwc_img)
    draw.ellipse([20, 20, 180, 180], outline=(150, 0, 0), width=8)
    draw.text((SIZE//2, SIZE//2), "FIFA\n2026", fill=(150, 0, 0), anchor="mm", align="center")
    fwc_img.save(fwc_path, "JPEG", quality=95)
    print("  ✅ FWC-1.jpg (placeholder)")

print("\n=== Normalizando TODOS los escudos a 200x200 fondo blanco ===")
normalized = 0
for fname in os.listdir(OUT):
    if not fname.endswith("-1.jpg"):
        continue
    path = os.path.join(OUT, fname)
    try:
        existing = Image.open(path)
        if existing.size == (SIZE, SIZE):
            continue  # ya está bien
        final = to_square_white(existing)
        final.save(path, "JPEG", quality=95)
        normalized += 1
        print(f"  📐 {fname}: {existing.size} → {SIZE}x{SIZE}")
    except Exception as e:
        print(f"  ⚠️  {fname}: {e}")

print(f"\nNormalizados: {normalized} escudos adicionales")

# Verificación final
total = sum(1 for f in os.listdir(OUT) if f.endswith("-1.jpg"))
print(f"\n=== TOTAL escudos -1.jpg: {total}/50 ===")
missing = []
ALL_CODES = ["FWC","MEX","RSA","KOR","CZE","CAN","BIH","QAT","SUI","BRA","MAR","HAI","SCO",
             "USA","PAR","AUS","TUR","GER","COW","CIV","ECU","NED","JPN","SWE","TUN","BEL",
             "EGY","IRN","NZL","ESP","CPV","KSA","URU","FRA","SEN","IRQ","NOR","ARG","ALG",
             "AUT","JOR","POR","COD","UZB","COL","ENG","CRO","GHA","PAN","CC"]
for c in ALL_CODES:
    if not os.path.exists(os.path.join(OUT, f"{c}-1.jpg")):
        missing.append(c)
if missing:
    print(f"Faltan: {missing}")
else:
    print("✅ Todos los 50 escudos presentes!")
