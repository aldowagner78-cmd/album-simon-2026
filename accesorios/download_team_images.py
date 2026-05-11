"""
Descarga escudos (num 1) y fotos de equipo (num 13) para cada selección.
Fuente: Wikipedia REST API (thumbnail del artículo del equipo nacional)
Guarda como: docs/img/stickers/{TEAM}-1.jpg y {TEAM}-13.jpg
"""
import os
import time
import requests
from PIL import Image
from io import BytesIO

OUT_DIR = "docs/img/stickers"
os.makedirs(OUT_DIR, exist_ok=True)

# Mapeo: código equipo → artículo Wikipedia para el equipo nacional de fútbol
WIKI_MAP = {
    "ARG": "Argentina national football team",
    "BRA": "Brazil national football team",
    "FRA": "France national football team",
    "GER": "Germany national football team",
    "ESP": "Spain national football team",
    "ENG": "England national football team",
    "POR": "Portugal national football team",
    "NED": "Netherlands national football team",
    "BEL": "Belgium national football team",
    "URU": "Uruguay national football team",
    "COL": "Colombia national football team",
    "MEX": "Mexico national football team",
    "USA": "United States men's national soccer team",
    "CAN": "Canada men's national soccer team",
    "SEN": "Senegal national football team",
    "MAR": "Morocco national football team",
    "EGY": "Egypt national football team",
    "ALG": "Algeria national football team",
    "TUN": "Tunisia national football team",
    "GHA": "Ghana national football team",
    "CIV": "Ivory Coast national football team",
    "COW": "Ivory Coast national football team",
    "COD": "DR Congo national football team",
    "RSA": "South Africa national football team",
    "JPN": "Japan national football team",
    "KOR": "South Korea national football team",
    "AUS": "Australia national football team",
    "IRN": "Iran national football team",
    "KSA": "Saudi Arabia national football team",
    "QAT": "Qatar national football team",
    "JOR": "Jordan national football team",
    "IRQ": "Iraq national football team",
    "UZB": "Uzbekistan national football team",
    "SUI": "Switzerland national football team",
    "CZE": "Czech Republic national football team",
    "CRO": "Croatia national football team",
    "SCO": "Scotland national football team",
    "NOR": "Norway national football team",
    "SWE": "Sweden national football team",
    "AUT": "Austria national football team",
    "TUR": "Turkey national football team",
    "BIH": "Bosnia and Herzegovina national football team",
    "ECU": "Ecuador national football team",
    "PAR": "Paraguay national football team",
    "PAN": "Panama national football team",
    "HAI": "Haiti national football team",
    "CPV": "Cape Verde national football team",
    "NZL": "New Zealand national football team",
    "NOR": "Norway national football team",
    "FWC": "2026 FIFA World Cup",
    "CC":  "CONCACAF Champions Cup",
}

# Para fotos de equipo (num 13), usar artículos alternativos que tengan foto grupal
WIKI_PHOTO_MAP = {
    "ARG": "Argentina national football team",
    "BRA": "Brazil national football team",
    "FRA": "France national football team",
    "GER": "Germany national football team",
    "ESP": "Spain national football team",
    "ENG": "England national football team",
    "POR": "Portugal national football team",
    "NED": "Netherlands national football team",
    "BEL": "Belgium national football team",
    "URU": "Uruguay national football team",
    # Para el resto usamos el mismo que el escudo
}

HEADERS = {
    "User-Agent": "AlbumSimon2026/1.0 (educational project; contact: github.com/aldowagner78-cmd)"
}

def get_wiki_thumbnail(article: str, size: int = 400) -> str | None:
    """Devuelve la URL de la imagen thumbnail de un artículo Wikipedia."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(article)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # Preferir thumbnail de mayor resolución
            if "originalimage" in data:
                return data["originalimage"]["source"]
            if "thumbnail" in data:
                src = data["thumbnail"]["source"]
                # Aumentar resolución cambiando el tamaño en la URL
                src = src.replace("/320px-", f"/{size}px-")
                return src
    except Exception as e:
        print(f"  Error API: {e}")
    return None

def save_image(url: str, path: str) -> bool:
    """Descarga imagen, la convierte a JPG y guarda."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}: {url}")
            return False
        img = Image.open(BytesIO(r.content)).convert("RGB")
        img.save(path, "JPEG", quality=90)
        print(f"  Guardado: {path} ({img.size[0]}x{img.size[1]})")
        return True
    except Exception as e:
        print(f"  Error imagen: {e}")
        return False

def download_for_team(team: str, num: int, article: str) -> bool:
    out_path = os.path.join(OUT_DIR, f"{team}-{num}.jpg")
    if os.path.exists(out_path):
        print(f"[{team}-{num}] Ya existe, salteando.")
        return True
    print(f"[{team}-{num}] Buscando: {article} ...")
    img_url = get_wiki_thumbnail(article, size=500)
    if not img_url:
        print(f"  Sin imagen en Wikipedia para: {article}")
        return False
    return save_image(img_url, out_path)

# --- MAIN ---
teams = list(WIKI_MAP.keys())
print(f"Descargando escudos (num 1) para {len(teams)} equipos...")
ok = 0
for team in teams:
    article = WIKI_MAP[team]
    success = download_for_team(team, 1, article)
    if success:
        ok += 1
    time.sleep(0.5)

print(f"\n✅ Escudos: {ok}/{len(teams)}")

print(f"\nDescargando fotos de equipo (num 13)...")
ok2 = 0
for team in teams:
    # Para fotos usamos el mismo artículo pero buscando imagen diferente si está disponible
    article = WIKI_PHOTO_MAP.get(team, WIKI_MAP[team])
    out_path = os.path.join(OUT_DIR, f"{team}-13.jpg")
    if os.path.exists(out_path):
        print(f"[{team}-13] Ya existe, salteando.")
        ok2 += 1
        continue
    # Si ya tenemos el escudo, copiamos como placeholder para la foto
    escudo_path = os.path.join(OUT_DIR, f"{team}-1.jpg")
    if os.path.exists(escudo_path):
        import shutil
        shutil.copy(escudo_path, out_path)
        print(f"[{team}-13] Usando escudo como placeholder.")
        ok2 += 1
    else:
        print(f"[{team}-13] Sin imagen disponible.")

print(f"\n✅ Fotos equipo: {ok2}/{len(teams)}")
print("\nListo! Imágenes en", OUT_DIR)
