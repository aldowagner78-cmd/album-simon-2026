"""
Extrae los 48 escudos de escudos_fuente.JPG (todos correctos).
FWC y CC quedan como placeholder.
Todos normalizados a 200x200 fondo blanco.
"""
import os
from PIL import Image, ImageDraw

SRC  = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\escudos_fuente.JPG"
OUT  = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\img\stickers"
SIZE = 200
PAD  = 14

img = Image.open(SRC)
W, H = img.size  # 502, 357

half_w  = W / 2
row_h   = H / 6
title_h = 13
col_w   = half_w / 4

# Mapa completo: código → (side, row, col)
# side: 'L'=izquierda, 'R'=derecha | row: 0-5 | col: 0-3
ALL_POS = {
    # Izquierda
    "MEX": ('L',0,0), "RSA": ('L',0,1), "KOR": ('L',0,2), "CZE": ('L',0,3),
    "CAN": ('L',1,0), "BIH": ('L',1,1), "QAT": ('L',1,2), "SUI": ('L',1,3),
    "BRA": ('L',2,0), "MAR": ('L',2,1), "HAI": ('L',2,2), "SCO": ('L',2,3),
    "USA": ('L',3,0), "PAR": ('L',3,1), "AUS": ('L',3,2), "TUR": ('L',3,3),
    "GER": ('L',4,0), "COW": ('L',4,1), "CIV": ('L',4,2), "ECU": ('L',4,3),
    "NED": ('L',5,0), "JPN": ('L',5,1), "SWE": ('L',5,2), "TUN": ('L',5,3),
    # Derecha
    "BEL": ('R',0,0), "EGY": ('R',0,1), "IRN": ('R',0,2), "NZL": ('R',0,3),
    "ESP": ('R',1,0), "CPV": ('R',1,1), "KSA": ('R',1,2), "URU": ('R',1,3),
    "FRA": ('R',2,0), "SEN": ('R',2,1), "IRQ": ('R',2,2), "NOR": ('R',2,3),
    "ARG": ('R',3,0), "ALG": ('R',3,1), "AUT": ('R',3,2), "JOR": ('R',3,3),
    "POR": ('R',4,0), "COD": ('R',4,1), "UZB": ('R',4,2), "COL": ('R',4,3),
    "ENG": ('R',5,0), "CRO": ('R',5,1), "GHA": ('R',5,2), "PAN": ('R',5,3),
}

def crop_shield(side, row, col):
    x0 = (0 if side == 'L' else half_w) + col * col_w + 2
    x1 = x0 + col_w - 4
    y0 = row * row_h + title_h + 1
    y1 = (row + 1) * row_h - 2
    return img.crop((int(x0), int(y0), int(x1), int(y1)))

def to_square_white(shield_img):
    shield_img = shield_img.convert("RGBA")
    shield_img.thumbnail((SIZE - PAD*2, SIZE - PAD*2), Image.LANCZOS)
    bg = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    sw, sh = shield_img.size
    bg.paste(shield_img, ((SIZE-sw)//2, (SIZE-sh)//2), shield_img.split()[3])
    return bg

# Borrar todos los -1.jpg existentes incorrectos
print("Borrando escudos incorrectos...")
for f in os.listdir(OUT):
    if f.endswith("-1.jpg"):
        os.remove(os.path.join(OUT, f))
print(f"Borrados.\n")

# Extraer los 48 desde la imagen fuente
print("=== Extrayendo 48 escudos de escudos_fuente.JPG ===")
ok = 0
for code, (side, row, col) in ALL_POS.items():
    shield = crop_shield(side, row, col)
    final  = to_square_white(shield)
    path   = os.path.join(OUT, f"{code}-1.jpg")
    final.save(path, "JPEG", quality=95)
    ok += 1
    print(f"  ✅ {code}")

# FWC - Copa del Mundo placeholder
fwc = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
d = ImageDraw.Draw(fwc)
d.ellipse([15,15,185,185], outline=(180,140,0), width=10)
d.text((SIZE//2, SIZE//2-12), "FIFA", fill=(180,140,0), anchor="mm")
d.text((SIZE//2, SIZE//2+12), "2026", fill=(180,140,0), anchor="mm")
fwc.save(os.path.join(OUT, "FWC-1.jpg"), "JPEG", quality=95)
print("  ✅ FWC (placeholder copa)")

# CC - CONCACAF placeholder
cc = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
d = ImageDraw.Draw(cc)
d.ellipse([15,15,185,185], outline=(0,80,160), width=10)
d.text((SIZE//2, SIZE//2-12), "CON-", fill=(0,80,160), anchor="mm")
d.text((SIZE//2, SIZE//2+12), "CACAF", fill=(0,80,160), anchor="mm")
cc.save(os.path.join(OUT, "CC-1.jpg"), "JPEG", quality=95)
print("  ✅ CC (placeholder CONCACAF)")

# Verificación
ALL_CODES = ["FWC","MEX","RSA","KOR","CZE","CAN","BIH","QAT","SUI","BRA","MAR","HAI","SCO",
             "USA","PAR","AUS","TUR","GER","COW","CIV","ECU","NED","JPN","SWE","TUN","BEL",
             "EGY","IRN","NZL","ESP","CPV","KSA","URU","FRA","SEN","IRQ","NOR","ARG","ALG",
             "AUT","JOR","POR","COD","UZB","COL","ENG","CRO","GHA","PAN","CC"]
total    = sum(1 for c in ALL_CODES if os.path.exists(os.path.join(OUT, f"{c}-1.jpg")))
missing  = [c for c in ALL_CODES if not os.path.exists(os.path.join(OUT, f"{c}-1.jpg"))]
print(f"\n=== RESULTADO: {total}/50 escudos ===")
if missing:
    print(f"Faltan: {missing}")
else:
    print("✅ Los 50 escudos listos!")
