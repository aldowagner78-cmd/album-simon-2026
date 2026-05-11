"""
Descarga escudos oficiales de thesportsdb.com (API gratuita).
Guarda como docs/img/stickers/{TEAM}-1.jpg
Borra los {C}-13.jpg incorrectos (fotos equipo) - esos quedan vacíos.
"""
import os, time, requests
from PIL import Image
from io import BytesIO

OUT_DIR = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\img\stickers"
HEADERS = {"User-Agent": "AlbumSimon2026/1.0"}

# Mapeo código → nombre en thesportsdb
TEAM_NAMES = {
    "ARG": "Argentina",
    "BRA": "Brazil",
    "FRA": "France",
    "GER": "Germany",
    "ESP": "Spain",
    "ENG": "England",
    "POR": "Portugal",
    "NED": "Netherlands",
    "BEL": "Belgium",
    "URU": "Uruguay",
    "COL": "Colombia",
    "MEX": "Mexico",
    "USA": "United States",
    "CAN": "Canada",
    "SEN": "Senegal",
    "MAR": "Morocco",
    "EGY": "Egypt",
    "ALG": "Algeria",
    "TUN": "Tunisia",
    "GHA": "Ghana",
    "CIV": "Ivory Coast",
    "COD": "DR Congo",
    "RSA": "South Africa",
    "JPN": "Japan",
    "KOR": "South Korea",
    "AUS": "Australia",
    "IRN": "Iran",
    "KSA": "Saudi Arabia",
    "QAT": "Qatar",
    "JOR": "Jordan",
    "IRQ": "Iraq",
    "UZB": "Uzbekistan",
    "SUI": "Switzerland",
    "CZE": "Czech Republic",
    "CRO": "Croatia",
    "SCO": "Scotland",
    "NOR": "Norway",
    "SWE": "Sweden",
    "AUT": "Austria",
    "TUR": "Turkey",
    "BIH": "Bosnia and Herzegovina",
    "ECU": "Ecuador",
    "PAR": "Paraguay",
    "PAN": "Panama",
    "HAI": "Haiti",
    "CPV": "Cape Verde",
    "NZL": "New Zealand",
    "COW": "Curacao",
    "ENG": "England",
    "CRO": "Croatia",
    "GHA": "Ghana",
}

def get_badge_url(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={requests.utils.quote(team_name)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        teams = data.get("teams") or []
        # Buscar el que sea selección nacional (idSport=Soccer, strSport=Soccer)
        for t in teams:
            badge = t.get("strTeamBadge") or t.get("strBadge")
            if badge:
                return badge
    except Exception as e:
        print(f"  Error: {e}")
    return None

def download_image(img_url, out_path):
    try:
        r = requests.get(img_url + "/preview", headers=HEADERS, timeout=20)
        if r.status_code != 200:
            # Try without /preview
            r = requests.get(img_url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return False
        img = Image.open(BytesIO(r.content)).convert("RGBA")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "RGBA":
            bg.paste(img, mask=img.split()[3])
        else:
            bg = img.convert("RGB")
        bg.save(out_path, "JPEG", quality=92)
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

print("=== PASO 1: Borrar {C}-13.jpg incorrectos ===")
deleted = 0
for f in os.listdir(OUT_DIR):
    if f.endswith("-13.jpg"):
        os.remove(os.path.join(OUT_DIR, f))
        deleted += 1
print(f"Borrados {deleted} archivos -13.jpg\n")

print("=== PASO 2: Descargar escudos oficiales ===")
ok = 0
fail = []
for code, name in TEAM_NAMES.items():
    out_path = os.path.join(OUT_DIR, f"{code}-1.jpg")
    # Borrar el existente incorrecto
    if os.path.exists(out_path):
        os.remove(out_path)

    print(f"[{code}] {name}...", end=" ", flush=True)
    badge_url = get_badge_url(name)
    if not badge_url:
        print(f"❌ Sin escudo en thesportsdb")
        fail.append(code)
        time.sleep(0.3)
        continue

    if download_image(badge_url, out_path):
        print(f"✅")
        ok += 1
    else:
        print(f"❌ Error descarga")
        fail.append(code)
    time.sleep(0.4)

# FWC y CC - escudo genérico (copa del mundo / concacaf)
for code, name in [("FWC", "FIFA World Cup"), ("CC", "CONCACAF")]:
    out_path = os.path.join(OUT_DIR, f"{code}-1.jpg")
    if os.path.exists(out_path):
        os.remove(out_path)
    print(f"[{code}] {name}...", end=" ", flush=True)
    badge_url = get_badge_url(name)
    if badge_url and download_image(badge_url, out_path):
        print("✅"); ok += 1
    else:
        print("❌ Sin imagen"); fail.append(code)
    time.sleep(0.4)

print(f"\n=== RESULTADO: {ok}/{len(TEAM_NAMES)+2} escudos OK ===")
if fail:
    print(f"Fallidos: {fail}")
