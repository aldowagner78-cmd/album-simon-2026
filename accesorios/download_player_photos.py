"""
Descarga fotos de jugadores desde Wikipedia REST API.
Indexadas por número Scanini correcto.
Guarda como: docs/img/stickers/{TEAM}-{NUM}.jpg
Sobreescribe archivos existentes (la numeración vieja era incorrecta).
Respeta rate limits con backoff.
"""
import os, json, time, requests
from PIL import Image
from io import BytesIO

OUT_DIR = "docs/img/stickers"
os.makedirs(OUT_DIR, exist_ok=True)

COUNTRIES = ["FWC","MEX","RSA","KOR","CZE","CAN","BIH","QAT","SUI","BRA","MAR","HAI",
             "SCO","USA","PAR","AUS","TUR","GER","COW","CIV","ECU","NED","JPN","SWE",
             "TUN","CC","BEL","EGY","IRN","NZL","ESP","CPV","KSA","URU","FRA","SEN",
             "IRQ","NOR","ARG","ALG","AUT","JOR","POR","COD","UZB","COL","ENG","CRO","GHA","PAN"]

HEADERS = {"User-Agent": "AlbumSimon2026/1.0 (educational; github.com/aldowagner78-cmd)"}

# Cache de fotos ya descargadas en esta sesion
DONE_FILE = "photos_done.json"
done = {}
if os.path.exists(DONE_FILE):
    with open(DONE_FILE, encoding="utf-8") as f:
        done = json.load(f)

with open("stickers_scanini.json", encoding="utf-8") as f:
    scanini = json.load(f)

def get_wiki_photo(name: str):
    """Devuelve URL de imagen desde Wikipedia REST API."""
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(name)
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  [429 - esperando {wait}s]", flush=True)
                time.sleep(wait)
                continue
            if r.status_code == 200:
                data = r.json()
                if "originalimage" in data:
                    return data["originalimage"]["source"]
                if "thumbnail" in data:
                    src = data["thumbnail"]["source"]
                    # Aumentar resolución
                    import re
                    src = re.sub(r'/(\d+)px-', '/500px-', src)
                    return src
            return None
        except Exception as e:
            print(f"  Error: {e}", flush=True)
            return None
    return None

def save_photo(img_url: str, path: str) -> bool:
    try:
        r = requests.get(img_url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return False
        # Rechazar SVGs (no son fotos de personas)
        ct = r.headers.get("content-type", "")
        if "svg" in ct or img_url.lower().endswith(".svg"):
            return False
        img = Image.open(BytesIO(r.content)).convert("RGB")
        w, h = img.size
        # Imagen demasiado pequeña = icono o logo, no foto
        if w < 80 or h < 80:
            return False
        # Recortar a formato retrato si es muy ancha
        if w > h:
            crop = img.crop(((w - h) // 2, 0, (w + h) // 2, h))
            crop.save(path, "JPEG", quality=88)
        else:
            img.save(path, "JPEG", quality=88)
        return True
    except Exception as e:
        print(f"  Error guardando: {e}", flush=True)
        return False

total = ok = skip = fail = 0
save_every = 20
count_since_save = 0

for team in COUNTRIES:
    team_data = scanini.get(team, {})
    for num_str in sorted(team_data.keys(), key=lambda x: int(x)):
        s = team_data[num_str]
        stype = s.get("type", "")
        # Saltar logos, fotos de equipo y specials (ya descargados)
        if "logo" in stype or "photo" in stype or "special" in stype:
            continue
        name = s.get("name", "")
        if not name or name in ("Team Logo", "Team Photo"):
            continue

        key = f"{team}-{num_str}"
        path = os.path.join(OUT_DIR, f"{key}.jpg")

        # Si ya está en done (descargado en sesión anterior), saltar
        if done.get(key) == "ok":
            skip += 1
            continue

        total += 1
        print(f"[{key}] {name}...", end=" ", flush=True)

        img_url = get_wiki_photo(name)
        if img_url:
            if save_photo(img_url, path):
                print("✓", flush=True)
                ok += 1
                done[key] = "ok"
            else:
                print("✗ (error guardando)", flush=True)
                fail += 1
        else:
            print("✗ (sin foto)", flush=True)
            fail += 1
            done[key] = "no_photo"

        count_since_save += 1
        if count_since_save >= save_every:
            with open(DONE_FILE, "w", encoding="utf-8") as f:
                json.dump(done, f)
            count_since_save = 0

        time.sleep(0.4)

# Guardar estado final
with open(DONE_FILE, "w", encoding="utf-8") as f:
    json.dump(done, f)

print(f"\n{'='*50}")
print(f"Descargados: {ok} | Sin foto: {fail} | Saltados: {skip} | Total procesados: {total}")
print(f"Fotos en: {OUT_DIR}")
