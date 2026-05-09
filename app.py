from __future__ import annotations

import json
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
ALBUM_FILE = BASE_DIR / "album_simon.json"
STATIC_IMG_DIR = BASE_DIR / "static" / "img"

app = Flask(__name__)

ALBUM_LOCK = threading.Lock()

COUNTRY_LABELS = {
    "FWC": "Mundial 2026",
    "MEX": "México",
    "RSA": "Sudáfrica",
    "KOR": "Corea del Sur",
    "CZE": "República Checa",
    "CAN": "Canadá",
    "BIH": "Bosnia y Herzegovina",
    "QAT": "Qatar",
    "SUI": "Suiza",
    "BRA": "Brasil",
    "MAR": "Marruecos",
    "HAI": "Haití",
    "SCO": "Escocia",
    "USA": "Estados Unidos",
    "PAR": "Paraguay",
    "AUS": "Australia",
    "TUR": "Turquía",
    "GER": "Alemania",
    "COW": "Costa de Marfil",
    "CIV": "Costa de Marfil",
    "ECU": "Ecuador",
    "NED": "Países Bajos",
    "JPN": "Japón",
    "SWE": "Suecia",
    "TUN": "Túnez",
    "CC": "Coca-Cola",
    "BEL": "Bélgica",
    "EGY": "Egipto",
    "IRN": "Irán",
    "NZL": "Nueva Zelanda",
    "ESP": "España",
    "CPV": "Cabo Verde",
    "KSA": "Arabia Saudita",
    "URU": "Uruguay",
    "FRA": "Francia",
    "SEN": "Senegal",
    "IRQ": "Irak",
    "NOR": "Noruega",
    "ARG": "Argentina",
    "ALG": "Argelia",
    "AUT": "Austria",
    "JOR": "Jordania",
    "POR": "Portugal",
    "COD": "R. D. del Congo",
    "UZB": "Uzbekistán",
    "COL": "Colombia",
    "ENG": "Inglaterra",
    "CRO": "Croacia",
    "GHA": "Ghana",
    "PAN": "Panamá",
}

COUNTRY_ORDER = [
    "FWC",
    "MEX",
    "RSA",
    "KOR",
    "CZE",
    "CAN",
    "BIH",
    "QAT",
    "SUI",
    "BRA",
    "MAR",
    "HAI",
    "SCO",
    "USA",
    "PAR",
    "AUS",
    "TUR",
    "GER",
    "COW",
    "CIV",
    "ECU",
    "NED",
    "JPN",
    "SWE",
    "TUN",
    "CC",
    "BEL",
    "EGY",
    "IRN",
    "NZL",
    "ESP",
    "CPV",
    "KSA",
    "URU",
    "FRA",
    "SEN",
    "IRQ",
    "NOR",
    "ARG",
    "ALG",
    "AUT",
    "JOR",
    "POR",
    "COD",
    "UZB",
    "COL",
    "ENG",
    "CRO",
    "GHA",
    "PAN",
]

MISSING = {
    "FWC": {2, 3, 4, 5, 12, 14},
    "MEX": {6, 7, 10, 11, 15, 16, 19, 20},
    "RSA": {2, 8, 9, 10, 11, 12, 14, 15, 17, 18, 19},
    "KOR": {11, 16, 20},
    "CZE": {1, 4, 9, 18},
    "CAN": {4, 8, 16, 17, 18, 20},
    "BIH": {4, 8, 12, 14, 17, 18},
    "QAT": {1, 3, 5, 11, 12, 17},
    "SUI": {2, 4, 6, 8, 9, 12, 17, 18},
    "BRA": {9, 11, 12},
    "MAR": {1, 2, 3, 4, 6, 7, 10, 11, 12, 14, 17, 18},
    "HAI": {2, 3, 4, 6, 7, 8, 10, 11, 12, 15, 16, 20},
    "SCO": {2, 6, 10, 15, 18},
    "USA": {5, 9},
    "PAR": {2, 3, 4, 5, 8, 9, 13, 14, 18},
    "AUS": {3, 5},
    "TUR": {3, 7, 15, 16, 20},
    "GER": {1},
    "COW": {7, 11, 17, 20},
    "CIV": {2, 3, 5, 9, 14, 16},
    "ECU": {1},
    "NED": {4, 5, 8, 9, 12, 13},
    "JPN": {1, 2, 3, 5, 13},
    "SWE": {4, 5, 14, 18},
    "TUN": {2, 4, 7, 8, 10, 11, 12, 15},
    "CC": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
    "BEL": {5, 9, 12, 13, 15, 17, 19},
    "EGY": {1, 3, 8, 11, 12, 13, 15, 16, 17, 19},
    "IRN": {4, 5, 8, 9, 14, 18},
    "NZL": {3, 7},
    "ESP": {1, 3, 7, 11, 16, 20},
    "CPV": {2, 5, 6, 11, 16},
    "KSA": {1, 12, 14, 18},
    "URU": {4, 5, 6, 8, 11, 15, 19, 20},
    "FRA": {1, 3, 7, 8, 9, 11, 14, 18},
    "SEN": {2, 7, 8, 10, 11, 12, 16, 19},
    "IRQ": {2, 3, 7, 10, 13, 15},
    "NOR": {11},
    "ARG": {5, 7, 9, 11, 14, 16, 18, 20},
    "ALG": {12, 17},
    "AUT": {9, 10, 14, 16, 20},
    "JOR": {3, 7, 9, 11, 16, 18},
    "POR": {2, 3, 6, 7, 10, 11, 15, 16, 19, 20},
    "COD": {15, 19},
    "UZB": {2, 6, 20},
    "COL": {1, 13, 20},
    "ENG": {2, 4, 6, 9, 14, 17, 18},
    "CRO": {2, 4, 6, 8, 10, 12, 15, 20},
    "GHA": {1, 13, 18, 19},
    "PAN": {4, 5, 8, 9, 10, 12, 14, 15, 17, 18, 20},
}


def ensure_album_exists() -> None:
    if ALBUM_FILE.exists():
        return
    with ALBUM_LOCK:
        if ALBUM_FILE.exists():
            return
        data = build_default_album()
        save_album(data)


def build_default_album() -> dict:
    stickers: list[dict] = []
    for codigo in COUNTRY_ORDER:
        missing = MISSING.get(codigo, set())
        for numero in range(1, 21):
            stickers.append(
                {
                    "codigo_pais": codigo,
                    "numero": numero,
                    "la_tengo": numero not in missing,
                    "repetidas": 0,
                }
            )
    return {"version": 1, "stickers": stickers}


def load_album() -> dict:
    ensure_album_exists()
    with ALBUM_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_album(data: dict) -> None:
    with ALBUM_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def get_sticker_map(data: dict) -> dict[tuple[str, int], dict]:
    return {
        (item["codigo_pais"], int(item["numero"])): item
        for item in data.get("stickers", [])
    }


def resolve_asset_path(codigo: str) -> str:
    for extension in ("svg", "png", "webp", "jpg", "jpeg"):
        candidate = STATIC_IMG_DIR / f"{codigo.lower()}.{extension}"
        if candidate.exists():
            return url_for("static", filename=f"img/{codigo.lower()}.{extension}")
    default_asset = STATIC_IMG_DIR / "default-shield.svg"
    if default_asset.exists():
        return url_for("static", filename="img/default-shield.svg")
    return url_for("static", filename=f"img/{codigo.lower()}.svg")


def build_album_view() -> list[dict]:
    data = load_album()
    sticker_map = get_sticker_map(data)
    countries: list[dict] = []

    for codigo in COUNTRY_ORDER:
        stickers = []
        for numero in range(1, 21):
            sticker = sticker_map[(codigo, numero)]
            stickers.append(sticker)
        countries.append(
            {
                "codigo": codigo,
                "nombre": COUNTRY_LABELS.get(codigo, codigo),
                "imagen": resolve_asset_path(codigo),
                "stickers": stickers,
            }
        )
    return countries


def normalize_boolean(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "on"}
    return bool(value)


def normalize_repeat(value) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def collect_album_lists() -> tuple[list[dict], list[dict]]:
    data = load_album()
    sticker_map = get_sticker_map(data)

    missing_by_country: list[dict] = []
    repeated_items: list[dict] = []

    for codigo in COUNTRY_ORDER:
        missing_numbers = []
        for numero in range(1, 21):
            sticker = sticker_map[(codigo, numero)]
            if not sticker["la_tengo"]:
                missing_numbers.append(numero)
            if sticker.get("repetidas", 0) > 0:
                repeated_items.append(
                    {
                        "codigo_pais": codigo,
                        "numero": numero,
                        "repetidas": int(sticker["repetidas"]),
                    }
                )

        if missing_numbers:
            missing_by_country.append(
                {
                    "codigo_pais": codigo,
                    "nombre": COUNTRY_LABELS.get(codigo, codigo),
                    "numeros": missing_numbers,
                }
            )

    return missing_by_country, repeated_items


def format_summary_text(missing_by_country: list[dict], repeated_items: list[dict]) -> str:
    missing_lines = ["Figuritas que me faltan"]
    if missing_by_country:
        for country in missing_by_country:
            numeros = ", ".join(str(n) for n in country["numeros"])
            missing_lines.append(f"{country['nombre']} ({country['codigo_pais']}): {numeros}")
    else:
        missing_lines.append("No faltan figuritas.")

    repeated_lines = ["Figuritas repetidas"]
    if repeated_items:
        for item in repeated_items:
            repeated_lines.append(f"{item['codigo_pais']} {item['numero']}: {item['repetidas']}")
    else:
        repeated_lines.append("No hay repetidas registradas.")

    return "\n".join(missing_lines + [""] + repeated_lines)


def normalize_numbers_by_country(payload: dict) -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    if not isinstance(payload, dict):
        return out

    for raw_code, raw_values in payload.items():
        if not isinstance(raw_code, str):
            continue
        code = raw_code.strip().upper()
        if not code:
            continue

        values: list[int] = []
        if isinstance(raw_values, list):
            for value in raw_values:
                try:
                    number = int(value)
                except (TypeError, ValueError):
                    continue
                if 1 <= number <= 20:
                    values.append(number)
        out[code] = set(values)

    return out


def compute_trade_suggestions(friend_missing: dict[str, set[int]], friend_repeated: dict[str, set[int]]) -> dict:
    own_missing, own_repeated_items = collect_album_lists()

    own_missing_map = {
        entry["codigo_pais"]: set(entry["numeros"])
        for entry in own_missing
    }
    own_repeated_map: dict[str, set[int]] = {}
    for item in own_repeated_items:
        own_repeated_map.setdefault(item["codigo_pais"], set()).add(item["numero"])

    friend_can_give = []
    simon_can_give = []
    mutual = []

    all_codes = sorted(set(COUNTRY_ORDER) | set(friend_missing) | set(friend_repeated) | set(own_missing_map) | set(own_repeated_map))
    for code in all_codes:
        friend_gives_numbers = sorted(friend_repeated.get(code, set()) & own_missing_map.get(code, set()))
        simon_gives_numbers = sorted(own_repeated_map.get(code, set()) & friend_missing.get(code, set()))

        if friend_gives_numbers:
            friend_can_give.append({"codigo_pais": code, "numeros": friend_gives_numbers})
        if simon_gives_numbers:
            simon_can_give.append({"codigo_pais": code, "numeros": simon_gives_numbers})
        if friend_gives_numbers and simon_gives_numbers:
            mutual.append(
                {
                    "codigo_pais": code,
                    "tu_recibes": friend_gives_numbers,
                    "tu_das": simon_gives_numbers,
                }
            )

    return {
        "friend_can_give": friend_can_give,
        "simon_can_give": simon_can_give,
        "mutual_suggestions": mutual,
    }


@app.get("/")
def index():
    return render_template("index.html", countries=build_album_view())


@app.get("/api/album")
def api_album():
    return jsonify(load_album())


@app.patch("/api/sticker/<codigo>/<int:numero>")
def update_sticker(codigo: str, numero: int):
    payload = request.get_json(silent=True) or {}
    with ALBUM_LOCK:
        data = load_album()
        sticker_map = get_sticker_map(data)
        sticker = sticker_map.get((codigo, numero))
        if sticker is None:
            return jsonify({"ok": False, "error": "Figurita no encontrada"}), 404

        if "la_tengo" in payload:
            sticker["la_tengo"] = normalize_boolean(payload["la_tengo"])
        if "repetidas" in payload:
            sticker["repetidas"] = normalize_repeat(payload["repetidas"])

        save_album(data)

    return jsonify({"ok": True, "sticker": sticker})


@app.post("/api/sticker/<codigo>/<int:numero>/toggle")
def toggle_sticker(codigo: str, numero: int):
    with ALBUM_LOCK:
        data = load_album()
        sticker_map = get_sticker_map(data)
        sticker = sticker_map.get((codigo, numero))
        if sticker is None:
            return jsonify({"ok": False, "error": "Figurita no encontrada"}), 404
        sticker["la_tengo"] = not bool(sticker.get("la_tengo", False))
        save_album(data)
    return jsonify({"ok": True, "sticker": sticker})


@app.get("/api/resumen")
def api_resumen():
    missing_by_country, repeated_items = collect_album_lists()

    return jsonify(
        {
            "missing_by_country": missing_by_country,
            "repeated_items": repeated_items,
            "summary_text": format_summary_text(missing_by_country, repeated_items),
        }
    )


@app.post("/api/compare")
def api_compare():
    payload = request.get_json(silent=True) or {}
    friend_missing = normalize_numbers_by_country(payload.get("friend_missing", {}))
    friend_repeated = normalize_numbers_by_country(payload.get("friend_repeated", {}))

    suggestions = compute_trade_suggestions(friend_missing, friend_repeated)
    return jsonify({"ok": True, **suggestions})


if __name__ == "__main__":
    ensure_album_exists()
    app.run(debug=True)