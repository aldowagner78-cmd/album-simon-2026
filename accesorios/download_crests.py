"""
Descarga escudos OFICIALES de cada selección.
Fuente: Wikipedia - busca en las imágenes del artículo la que tenga
'crest', 'badge', 'logo', 'emblem', 'coat' en el nombre del archivo.
Borra los {C}-1.jpg existentes y los reemplaza con el escudo correcto.
"""
import os, time, re, requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote

OUT_DIR = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\img\stickers"

HEADERS = {
    "User-Agent": "AlbumSimon2026/1.0 (educational; github.com/aldowagner78-cmd)"
}

# Artículo Wikipedia para cada selección
WIKI_MAP = {
    "FWC": "2026 FIFA World Cup",
    "MEX": "Mexico national football team",
    "RSA": "South Africa national football team",
    "KOR": "South Korea national football team",
    "CZE": "Czech Republic national football team",
    "CAN": "Canada men's national soccer team",
    "BIH": "Bosnia and Herzegovina national football team",
    "QAT": "Qatar national football team",
    "SUI": "Switzerland national football team",
    "BRA": "Brazil national football team",
    "MAR": "Morocco national football team",
    "HAI": "Haiti national football team",
    "SCO": "Scotland national football team",
    "USA": "United States men's national soccer team",
    "PAR": "Paraguay national football team",
    "AUS": "Australia national football team",
    "TUR": "Turkey national football team",
    "GER": "Germany national football team",
    "COW": "Curaçao national football team",
    "CIV": "Ivory Coast national football team",
    "ECU": "Ecuador national football team",
    "NED": "Netherlands national football team",
    "JPN": "Japan national football team",
    "SWE": "Sweden national football team",
    "TUN": "Tunisia national football team",
    "BEL": "Belgium national football team",
    "EGY": "Egypt national football team",
    "IRN": "Iran national football team",
    "NZL": "New Zealand men's national football team",
    "ESP": "Spain national football team",
    "CPV": "Cape Verde national football team",
    "KSA": "Saudi Arabia national football team",
    "URU": "Uruguay national football team",
    "FRA": "France national football team",
    "SEN": "Senegal national football team",
    "IRQ": "Iraq national football team",
    "NOR": "Norway national football team",
    "ARG": "Argentina national football team",
    "ALG": "Algeria national football team",
    "AUT": "Austria national football team",
    "JOR": "Jordan national football team",
    "POR": "Portugal national football team",
    "COD": "DR Congo national football team",
    "UZB": "Uzbekistan national football team",
    "COL": "Colombia national football team",
    "ENG": "England national football team",
    "CRO": "Croatia national football team",
    "GHA": "Ghana national football team",
    "PAN": "Panama national football team",
    "CC":  "CONCACAF Champions Cup",
}

KEYWORDS = ["crest", "badge", "logo", "emblem", "coat", "federation", "shield"]

def get_images_from_article(article):
    """Devuelve lista de {title, url} de imágenes del artículo Wikipedia."""
    url = (f"https://en.wikipedia.org/w/api.php"
           f"?action=query&titles={quote(article)}"
           f"&prop=images&imlimit=50&format=json&redirects=1")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            return [img["title"] for img in page.get("images", [])]
    except Exception as e:
        print(f"  Error query: {e}")
    return []

def get_image_url(file_title, size=400):
    """Obtiene la URL directa de un File: de Wikipedia."""
    url = (f"https://en.wikipedia.org/w/api.php"
           f"?action=query&titles={quote(file_title)}"
           f"&prop=imageinfo&iiprop=url&iiurlwidth={size}&format=json")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            ii = page.get("imageinfo", [])
            if ii:
                return ii[0].get("thumburl") or ii[0].get("url")
    except Exception as e:
        print(f"  Error imageinfo: {e}")
    return None

def find_crest_title(image_titles, team_code):
    """Busca entre los títulos de imagen el que sea el escudo."""
    lower = [t.lower() for t in image_titles]
    # Prioridad: archivos SVG/PNG/JPG con keywords de escudo
    for kw in KEYWORDS:
        for i, t in enumerate(lower):
            if kw in t and not any(x in t for x in ["kit", "away", "home", "jersey", "shirt", "captain", "flag", "map", "stadium"]):
                return image_titles[i]
    return None

def download_image(img_url, out_path):
    try:
        r = requests.get(img_url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return False
        img = Image.open(BytesIO(r.content)).convert("RGBA")
        # Fondo blanco para SVG/PNG transparente
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "RGBA":
            bg.paste(img, mask=img.split()[3])
        else:
            bg.paste(img)
        bg.save(out_path, "JPEG", quality=92)
        return True
    except Exception as e:
        print(f"  Error guardando: {e}")
        return False

ok = 0
fail = []
teams = list(WIKI_MAP.keys())
print(f"Descargando escudos para {len(teams)} equipos...\n")

for team in teams:
    article = WIKI_MAP[team]
    out_path = os.path.join(OUT_DIR, f"{team}-1.jpg")

    # Borrar el existente incorrecto
    if os.path.exists(out_path):
        os.remove(out_path)

    print(f"[{team}] {article}")
    images = get_images_from_article(article)
    if not images:
        print(f"  Sin imágenes en Wikipedia")
        fail.append(team)
        time.sleep(0.5)
        continue

    crest_title = find_crest_title(images, team)
    if not crest_title:
        print(f"  No encontré escudo entre {len(images)} imágenes: {[t.split(':')[1][:40] for t in images[:5]]}")
        fail.append(team)
        time.sleep(0.5)
        continue

    print(f"  Escudo: {crest_title.split(':')[1][:60]}")
    img_url = get_image_url(crest_title, size=400)
    if not img_url:
        print(f"  Sin URL de imagen")
        fail.append(team)
        time.sleep(0.5)
        continue

    if download_image(img_url, out_path):
        print(f"  ✅ Guardado")
        ok += 1
    else:
        print(f"  ❌ Error descarga")
        fail.append(team)
    time.sleep(0.6)

print(f"\n=== RESULTADO: {ok}/{len(teams)} escudos OK ===")
if fail:
    print(f"Fallidos: {fail}")
