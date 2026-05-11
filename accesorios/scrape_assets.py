"""Generador/descargador curado de assets para el album.

Objetivo:
- Evitar scraping aleatorio de baja calidad.
- Usar fuentes consistentes y publicas para banderas (SVG) por pais.
- Generar logos locales limpios para codigos especiales (FWC y CC).

Salida:
- Archivos en static/img/<codigo>.svg

Uso:
    py scrape_assets.py
"""

from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "static" / "img"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

# Codigo del album -> ISO2 para usar flagcdn (SVG)
COUNTRY_TO_ISO2 = {
    "MEX": "mx",
    "RSA": "za",
    "KOR": "kr",
    "CZE": "cz",
    "CAN": "ca",
    "BIH": "ba",
    "QAT": "qa",
    "SUI": "ch",
    "BRA": "br",
    "MAR": "ma",
    "HAI": "ht",
    "SCO": "gb-sct",
    "USA": "us",
    "PAR": "py",
    "AUS": "au",
    "TUR": "tr",
    "GER": "de",
    "COW": "ci",
    "CIV": "ci",
    "ECU": "ec",
    "NED": "nl",
    "JPN": "jp",
    "SWE": "se",
    "TUN": "tn",
    "BEL": "be",
    "EGY": "eg",
    "IRN": "ir",
    "NZL": "nz",
    "ESP": "es",
    "CPV": "cv",
    "KSA": "sa",
    "URU": "uy",
    "FRA": "fr",
    "SEN": "sn",
    "IRQ": "iq",
    "NOR": "no",
    "ARG": "ar",
    "ALG": "dz",
    "AUT": "at",
    "JOR": "jo",
    "POR": "pt",
    "COD": "cd",
    "UZB": "uz",
    "COL": "co",
    "ENG": "gb-eng",
    "CRO": "hr",
    "GHA": "gh",
    "PAN": "pa",
}


def normalize_flagcdn_url(iso2: str) -> str:
    # Para casos especiales de subdivisions en FlagCDN (gb-eng, gb-sct) usamos endpoint /w320/
    return f"https://flagcdn.com/{iso2}.svg"


def download_svg(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def save_svg(code: str, svg_text: str) -> None:
    path = OUTPUT_DIR / f"{code.lower()}.svg"
    path.write_text(svg_text, encoding="utf-8")


def build_special_fwc_logo() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" role="img" aria-label="Mundial 2026">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b3b7a"/>
      <stop offset="100%" stop-color="#1455a8"/>
    </linearGradient>
  </defs>
  <rect x="12" y="12" width="196" height="196" rx="36" fill="url(#bg)"/>
  <circle cx="110" cy="84" r="38" fill="#ffffff" fill-opacity="0.93"/>
  <path d="M72 130h76l-8 42H80z" fill="#f3c75b"/>
  <text x="110" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#0b3b7a">FWC</text>
  <text x="110" y="168" text-anchor="middle" font-family="Arial, sans-serif" font-size="34" font-weight="800" fill="#ffffff">26</text>
</svg>"""


def build_special_cc_logo() -> str:
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" role="img" aria-label="Coca-Cola estilo clasico">
    <defs>
        <linearGradient id="ccbg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#d71931"/>
            <stop offset="100%" stop-color="#a10c23"/>
        </linearGradient>
        <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.25"/>
        </filter>
    </defs>
    <rect x="12" y="12" width="196" height="196" rx="36" fill="url(#ccbg)"/>
    <path d="M28 132c24-18 56-14 80-2 20 10 46 18 84 0" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" opacity="0.9"/>
    <path d="M32 150c22-13 46-11 70-2 24 9 54 14 86-2" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.72"/>
    <text x="110" y="105" text-anchor="middle" font-family="Brush Script MT, Segoe Script, cursive" font-size="48" font-weight="700" fill="#ffffff" filter="url(#soft)">Coca-Cola</text>
    <text x="110" y="174" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" letter-spacing="1.2" fill="#ffd9a0">ESTILO CLASICO</text>
</svg>"""


def try_fetch_wikipedia_svg_title(title: str) -> str | None:
    """Usa BeautifulSoup para extraer un SVG principal de una pagina publica en Wikipedia.

    Se usa solo como extra curado, no como scraping masivo.
    """

    url = f"https://en.wikipedia.org/wiki/{title}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=25)
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.select_one("table.infobox img")
    if not image:
        return None

    src = image.get("src", "")
    if not src:
        return None
    if src.startswith("//"):
        src = "https:" + src
    if src.endswith(".svg") or ".svg" in src:
        try:
            return download_svg(src)
        except requests.RequestException:
            return None
    return None


def main() -> None:
    print(f"Generando assets en {OUTPUT_DIR}")

    # Limpieza controlada: dejamos solo archivos .svg generados en esta corrida
    for file in OUTPUT_DIR.glob("*.svg"):
        if file.name == "default-shield.svg":
            continue
        file.unlink(missing_ok=True)

    ok = 0
    fail = 0

    for code, iso2 in COUNTRY_TO_ISO2.items():
        url = normalize_flagcdn_url(iso2)
        try:
            svg = download_svg(url)
            save_svg(code, svg)
            print(f"[{code}] OK {url}")
            ok += 1
        except requests.RequestException as exc:
            print(f"[{code}] FAIL {exc}")
            fail += 1

    # Assets especiales por codigo del album
    save_svg("FWC", build_special_fwc_logo())
    save_svg("CC", build_special_cc_logo())

    # Fallback opcional: intentar icono de seleccion argentina desde Wikipedia
    arg_wiki = try_fetch_wikipedia_svg_title("Argentina_national_football_team")
    if arg_wiki:
        save_svg("arg_badge", arg_wiki)
        print("[ARG_BADGE] extra guardado desde Wikipedia")

    print(f"Listo. Exitos: {ok}, Fallos: {fail}, Especiales: 2")


if __name__ == "__main__":
    main()
