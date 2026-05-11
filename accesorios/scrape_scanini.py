"""
Scraper de Scanini: obtiene los nombres y el orden correcto de cada figurita
para los 50 equipos del álbum Panini FIFA World Cup 2026.
Luego enriquece con datos de jugadores (DOB, altura, peso, club) desde Wikipedia.
"""

import time
import csv
import re
import json
from urllib.request import urlopen, Request
from html.parser import HTMLParser

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; FigusScraper/1.0)"}

TEAMS = [
    ("FWC",  "world-cup-history"),
    ("ALG",  "algeria"),
    ("ARG",  "argentina"),
    ("AUS",  "australia"),
    ("AUT",  "austria"),
    ("BEL",  "belgium"),
    ("BIH",  "bosnia-and-herzegovina"),
    ("BRA",  "brazil"),
    ("CAN",  "canada"),
    ("CIV",  "cote-divoire"),
    ("COD",  "dr-congo"),
    ("COL",  "colombia"),
    ("CPV",  "cape-verde"),
    ("CRO",  "croatia"),
    ("CUW",  "curacao"),
    ("CZE",  "czechia"),
    ("ECU",  "ecuador"),
    ("EGY",  "egypt"),
    ("ENG",  "england"),
    ("ESP",  "spain"),
    ("FRA",  "france"),
    ("GER",  "germany"),
    ("GHA",  "ghana"),
    ("HAI",  "haiti"),
    ("IRN",  "iran"),
    ("IRQ",  "iraq"),
    ("JOR",  "jordan"),
    ("JPN",  "japan"),
    ("KOR",  "south-korea"),
    ("KSA",  "saudi-arabia"),
    ("MAR",  "morocco"),
    ("MEX",  "mexico"),
    ("NED",  "netherlands"),
    ("NOR",  "norway"),
    ("NZL",  "new-zealand"),
    ("PAN",  "panama"),
    ("PAR",  "paraguay"),
    ("POR",  "portugal"),
    ("QAT",  "qatar"),
    ("RSA",  "south-africa"),
    ("SCO",  "scotland"),
    ("SEN",  "senegal"),
    ("SUI",  "switzerland"),
    ("SWE",  "sweden"),
    ("TUN",  "tunisia"),
    ("TUR",  "turkey"),
    ("URU",  "uruguay"),
    ("USA",  "united-states"),
    ("UZB",  "uzbekistan"),
]

# Mapa code→slugs para PANINI (1 sticker) y FWC (19)
# Los que no están en la lista principal de 20 stickers

class ListParser(HTMLParser):
    """Extrae los items de la lista de figuritas de una página de equipo."""
    def __init__(self):
        super().__init__()
        self.stickers = []  # lista de (code, name, type)
        self._in_list = False
        self._in_item = False
        self._texts = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "li":
            self._in_item = True
            self._texts = []
        if tag == "a" and self._in_item:
            self._depth += 1

    def handle_endtag(self, tag):
        if tag == "li" and self._in_item:
            self._in_item = False
            # texts: ["CODE N", "Name", "type"]
            if len(self._texts) >= 2:
                parts = self._texts
                # e.g. ["ARG 17", "Lionel Messi", "player"]
                code_n = parts[0].strip() if parts else ""
                name = parts[1].strip() if len(parts) > 1 else ""
                stype = parts[2].strip() if len(parts) > 2 else ""
                if code_n and re.match(r"[A-Z]", code_n):
                    self.stickers.append((code_n, name, stype))

    def handle_data(self, data):
        if self._in_item:
            t = data.strip()
            if t:
                self._texts.append(t)


def fetch(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def scrape_team(slug):
    url = f"https://scanini.app/teams/{slug}"
    html = fetch(url)
    parser = ListParser()
    parser.feed(html)
    return parser.stickers


def main():
    rows = []
    for code, slug in TEAMS:
        print(f"  Scrapeando {code} ({slug})...", flush=True)
        try:
            stickers = scrape_team(slug)
            for item in stickers:
                code_n, name, stype = item
                # Parsear número
                m = re.match(r"([A-Z]+)\s+(\d+)", code_n)
                if m:
                    team_code = m.group(1)
                    num = int(m.group(2))
                else:
                    team_code = code
                    num = 0
                rows.append({
                    "team": team_code,
                    "num": num,
                    "name": name,
                    "type": stype,
                    "slug_url": f"https://scanini.app/teams/{slug}"
                })
            print(f"    -> {len(stickers)} stickers", flush=True)
        except Exception as e:
            print(f"    ERROR: {e}", flush=True)
        time.sleep(0.4)  # cortés con el servidor

    # Guardar CSV
    out_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["team","num","name","type","slug_url"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV guardado en: {out_path}")
    print(f"Total filas: {len(rows)}")

    # También guardar JSON para fácil uso en JS
    json_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.json"
    # Estructura: { "ARG": { 1: {name, type}, 2: {...}, ... }, ... }
    by_team = {}
    for r in rows:
        t = r["team"]
        if t not in by_team:
            by_team[t] = {}
        by_team[t][r["num"]] = {"name": r["name"], "type": r["type"]}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(by_team, f, ensure_ascii=False, indent=2)
    print(f"JSON guardado en: {json_path}")


if __name__ == "__main__":
    main()
