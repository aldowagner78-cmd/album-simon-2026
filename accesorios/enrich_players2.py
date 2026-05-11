"""
Enriquece jugadores con DOB, altura, peso, club via Wikipedia REST API.
Versión 2: encoding fix + parser mejorado + reintentos con variantes de nombre.
"""

import json, time, re, csv, sys
from urllib.request import urlopen, Request
from urllib.parse import quote

# Fix encoding en Windows
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

HEADERS = {"User-Agent": "Mozilla/5.0 (FigusScraper/2.0; educational)"}

# Variantes de nombre para jugadores con páginas de desambiguación
NAME_FIXES = {
    "Emiliano Martinez":    "Emiliano Martínez (footballer, born 1992)",
    "Nicolas Otamendi":     "Nicolás Otamendi",
    "Nicolas Tagliafico":   "Nicolás Tagliafico",
    "Lautaro Martinez":     "Lautaro Martínez",
    "Julian Alvarez":       "Julián Álvarez",
    "Lionel Messi":         "Lionel Messi",
    "Enzo Fernandez":       "Enzo Fernández",
    "Rodrigo De Paul":      "Rodrigo De Paul",
    "Alexis Mac Allister":  "Alexis Mac Allister",
    "Nico Paz":             "Nico Paz (footballer)",
    "Nico Gonzalez":        "Nico González (footballer)",
    "Ismael Bennacer":      "Ismaël Bennacer",
    "Houssem Aquar":        "Houssem Aouar",
    "Fares Chaibi":         "Farès Chaibi",
    "Said Benrahma":        "Saïd Benrahma",
    "Aissa Mandi":          "Aïssa Mandi",
    "Rayan At-Nouri":       "Rayan Aït-Nouri",
    "Mohamed Amine Tougai": "Mohamed Amine Tougaï",
    "Vinicius Junior":      "Vinicius Júnior",
    "Neymar Junior":        "Neymar",
    "Kylian Mbappe":        "Kylian Mbappé",
    "Erling Haaland":       "Erling Haaland",
    "Mohamed Salah":        "Mohamed Salah",
    "Son Heung-min":        "Son Heung-min",
    "Virgil van Dijk":      "Virgil van Dijk",
    "Kevin De Bruyne":      "Kevin De Bruyne",
    "Thibaut Courtois":     "Thibaut Courtois",
    "Phil Foden":           "Phil Foden",
    "Jude Bellingham":      "Jude Bellingham",
    "Bukayo Saka":          "Bukayo Saka",
    "Harry Kane":           "Harry Kane",
    "Marcus Rashford":      "Marcus Rashford",
    "Jamal Musiala":        "Jamal Musiala",
    "Florian Wirtz":        "Florian Wirtz",
    "Manuel Neuer":         "Manuel Neuer",
    "Thomas Müller":        "Thomas Müller",
    "Thomas Muller":        "Thomas Müller",
    "Robert Lewandowski":   "Robert Lewandowski",
    "Pedri":                "Pedri",
    "Gavi":                 "Gavi (footballer)",
    "Lamine Yamal":         "Lamine Yamal",
    "Dani Olmo":            "Dani Olmo",
    "Alvaro Morata":        "Álvaro Morata",
    "Antoine Griezmann":    "Antoine Griezmann",
    "Kylian Mbapp":         "Kylian Mbappé",
    "Ousmane Dembele":      "Ousmane Dembélé",
    "Ousmane Dembélé":      "Ousmane Dembélé",
    "Marcus Thuram":        "Marcus Thuram",
    "Aurelien Tchouameni":  "Aurélien Tchouaméni",
    "Aurélien Tchouaméni":  "Aurélien Tchouaméni",
    "Eduardo Camavinga":    "Eduardo Camavinga",
    "Randal Kolo Muani":    "Randal Kolo Muani",
    "William Saliba":       "William Saliba",
    "Theo Hernandez":       "Théo Hernández",
    "Dayot Upamecano":      "Dayot Upamecano",
    "Ruben Dias":           "Rúben Dias",
    "Bernardo Silva":       "Bernardo Silva",
    "Bruno Fernandes":      "Bruno Fernandes (Portuguese footballer)",
    "Rafael Leao":          "Rafael Leão",
    "Joao Felix":           "João Félix",
    "Diogo Jota":           "Diogo Jota",
    "Gonçalo Ramos":        "Gonçalo Ramos",
    "Goncalo Ramos":        "Gonçalo Ramos",
    "Cristiano Ronaldo":    "Cristiano Ronaldo",
    "Sadio Mane":           "Sadio Mané",
    "Kalidou Koulibaly":    "Kalidou Koulibaly",
    "Achraf Hakimi":        "Achraf Hakimi",
    "Sofyan Amrabat":       "Sofyan Amrabat",
    "Hakim Ziyech":         "Hakim Ziyech",
    "Darwin Nunez":         "Darwin Núñez",
    "Federico Valverde":    "Federico Valverde",
    "Paulo Dybala":         "Paulo Dybala",
    "Luka Modric":          "Luka Modrić",
    "Ivan Perisic":         "Ivan Perišić",
    "Josko Gvardiol":       "Joško Gvardiol",
    "Mateo Kovacic":        "Mateo Kovačić",
    "Aleksandar Mitrovic":  "Aleksandar Mitrović",
    "Dusan Vlahovic":       "Dušan Vlahović",
    "Granit Xhaka":         "Granit Xhaka",
    "Xherdan Shaqiri":      "Xherdan Shaqiri",
    "Breel Embolo":         "Breel Embolo",
    "Hakan Calhanoglu":     "Hakan Çalhanoğlu",
    "Arda Guler":           "Arda Güler",
    "Merih Demiral":        "Merih Demiral",
    "Caglar Soyuncu":       "Çağlar Söyüncü",
    "Thomas Partey":        "Thomas Partey",
    "André Ayew":           "André Ayew",
    "Jordan Ayew":          "Jordan Ayew",
    "Mohammed Kudus":       "Mohammed Kudus",
    "Inaki Williams":       "Iñaki Williams",
    "Kamaldeen Sulemana":   "Kamaldeen Sulemana",
    "Antoine Semenyo":      "Antoine Semenyo",
    "Franck Kessie":        "Franck Kessié",
    "Nicolas Pepe":         "Nicolas Pépé",
    "Sébastien Haller":     "Sébastien Haller",
    "Sebastien Haller":     "Sébastien Haller",
    "Jonathan Tah":         "Jonathan Tah",
    "Ilkay Gundogan":       "İlkay Gündoğan",
    "Kai Havertz":          "Kai Havertz",
    "Leroy Sane":           "Leroy Sané",
    "Serge Gnabry":         "Serge Gnabry",
    "Frenkie de Jong":      "Frenkie de Jong",
    "Xavi Simons":          "Xavi Simons",
    "Cody Gakpo":           "Cody Gakpo",
    "Memphis Depay":        "Memphis Depay",
    "Tijjani Reijnders":    "Tijjani Reijnders",
    "Denzel Dumfries":      "Denzel Dumfries",
    "Teun Koopmeiners":     "Teun Koopmeiners",
    "Ryan Gravenberch":     "Ryan Gravenberch",
    "Wout Weghorst":        "Wout Weghorst",
    "Martin Odegaard":      "Martin Ødegaard",
    "Erling Haaland":       "Erling Haaland",
    "Antonio Rudiger":      "Antonio Rüdiger",
    "Nico Schlotterbeck":   "Nico Schlotterbeck",
    "Leon Goretzka":        "Leon Goretzka",
    "Niclas Fullkrug":      "Niclas Füllkrug",
    "Sébastien Haller":     "Sébastien Haller",
    "Edin Dzeko":           "Edin Džeko",
    "Miralem Pjanic":       "Miralem Pjanić",
    "Sead Kolasinac":       "Sead Kolašinac",
    "Benjamin Sesko":       "Benjamin Šeško",
    "Amar Dedic":           "Amar Dedić",
    "Riyad Mahrez":         "Riyad Mahrez",
    "Lucas Paqueta":        "Lucas Paquetá",
    "Rodrygo":              "Rodrygo",
    "Raphinha":             "Raphinha",
    "Endrick":              "Endrick",
    "Alisson Becker":       "Alisson Becker",
    "Marquinhos":           "Marquinhos (footballer)",
    "Casemiro":             "Casemiro",
    "Bruno Guimaraes":      "Bruno Guimarães",
    "Rodri":                "Rodri",
    "Fabian Ruiz":          "Fabián Ruiz",
    "Ferran Torres":        "Ferran Torres",
    "Pedri":                "Pedri",
    "Unai Simon":           "Unai Simón",
    "David Raya":           "David Raya",
    "Dani Carvajal":        "Dani Carvajal",
    "Mikel Oyarzabal":      "Mikel Oyarzabal",
    "Nico Williams":        "Nico Williams (footballer)",
    "Luis Diaz":            "Luis Díaz (Colombian footballer)",
    "James Rodriguez":      "James Rodríguez",
    "Davinson Sanchez":     "Dávinson Sánchez",
    "Yerry Mina":           "Yerry Mina",
    "Juan Cuadrado":        "Juan Cuadrado",
    "Jhon Arias":           "Jhon Arias",
    "Richard Rios":         "Richard Ríos",
    "Jhon Duran":           "Jhon Jáder Durán",
    "Jhon Jader Duran":     "Jhon Jáder Durán",
    "Wataru Endo":          "Wataru Endō",
    "Kaoru Mitoma":         "Kaoru Mitoma",
    "Takumi Minamino":      "Takumi Minamino",
    "Ritsu Doan":           "Ritsu Dōan",
    "Ayase Ueda":           "Ayase Ueda",
    "Takefusa Kubo":        "Takefusa Kubo",
    "Ao Tanaka":            "Ao Tanaka",
    "Daizen Maeda":         "Daizen Maeda",
    "Kim Min-jae":          "Kim Min-jae (footballer)",
    "Lee Kang-in":          "Lee Kang-in",
    "Hwang Hee-chan":       "Hwang Hee-chan",
    "Cho Gue-sung":         "Cho Gue-sung",
    "Hwang In-beom":        "Hwang In-beom",
    "Mohamed Al-Owais":     "Mohammed Al-Owais",
    "Nasser Al-Dawsari":    "Nasser Al-Dawsari",
    "Salem Al-Dawsari":     "Salem Al-Dawsari",
    "Saud Abdulhamid":      "Saud Abdulhamid",
    "Akram Afif":           "Akram Afif",
    "Almoez Ali":           "Almoez Ali",
    "Hasan Al-Haydos":      "Hassan Al-Haydos",
    "Tariq Lamptey":        "Tariq Lamptey",
    "Alexandre Lacazette":  "Alexandre Lacazette",
    "Mathew Ryan":          "Mathew Ryan",
    "Aaron Mooy":           "Aaron Mooy",
    "Mathew Leckie":        "Mathew Leckie",
    "Mehdi Taremi":         "Mehdi Taremi",
    "Ali Gholizadeh":       "Ali Gholizadeh",
    "Sardar Azmoun":        "Sardar Azmoun",
    "Pablo Milad":          "Pablo Milad",
    "Yacine Brahimi":       "Yacine Brahimi",
    "Ali Al-Bulayhi":       "Ali Al-Bulayhi",
    "Cristian Romero":      "Cristián Romero",
    "Leandro Paredes":      "Leandro Paredes",
    "Exequiel Palacios":    "Exequiel Palacios",
    "Giuliano Simeone":     "Giuliano Simeone",
    "Gabriel Martinelli":   "Gabriel Martinelli",
    "Endrick":              "Endrick",
    "Santiago Gimenez":     "Santiago Giménez (footballer)",
    "Edson Alvarez":        "Edson Álvarez",
    "Hirving Lozano":       "Hirving Lozano",
    "Raul Jimenez":         "Raúl Jiménez",
    "Orbelin Pineda":       "Orbelin Pineda",
    "Alexis Vega":          "Alexis Vega (footballer)",
    "Alfredo Talavera":     "Alfredo Talavera",
    "Miguel Herrera":       "Miguel Herrera",
    "Robin Olsen":          "Robin Olsen",
    "Emil Forsberg":        "Emil Forsberg",
    "Dejan Kulusevski":     "Dejan Kulusevski",
    "Alexander Isak":       "Alexander Isak",
    "Victor Nilsson Lindelof": "Victor Lindelöf",
    "Facundo Torres":       "Facundo Torres (footballer, born 2001)",
    "Federico Valverde":    "Federico Valverde",
    "Darwin Núñez":         "Darwin Núñez",
    "Edinson Cavani":       "Edinson Cavani",
    "Luis Suarez":          "Luis Suárez",
    "Christian Pulisic":    "Christian Pulisic",
    "Weston McKennie":      "Weston McKennie",
    "Tyler Adams":          "Tyler Adams (soccer)",
    "Ricardo Pepi":         "Ricardo Pepi",
    "Folarin Balogun":      "Folarin Balogun",
    "Alphonso Davies":      "Alphonso Davies",
    "Jonathan David":       "Jonathan David (footballer)",
    "Cyle Larin":           "Cyle Larin",
    "Stephen Eustaquio":    "Stephen Eustáquio",
    "Tajon Buchanan":       "Tajon Buchanan",
    "Percy Tau":            "Percy Tau",
    "Lyle Foster":          "Lyle Foster",
    "Teboho Mokoena":       "Teboho Mokoena",
    "Evidence Makgopa":     "Evidence Makgopa",
    "Scott McTominay":      "Scott McTominay",
    "John McGinn":          "John McGinn",
    "Andy Robertson":       "Andy Robertson",
    "Kieran Tierney":       "Kieran Tierney",
    "Lyndon Dykes":         "Lyndon Dykes",
    "Lawrence Shankland":   "Lawrence Shankland",
    "Che Adams":            "Che Adams",
    "Billy Gilmour":        "Billy Gilmour",
    "Ellyes Skhiri":        "Ellyes Skhiri",
    "Wahbi Khazri":         "Wahbi Khazri",
    "Issam Jebali":         "Issam Jebali",
    "Hannibal Mejbri":      "Hannibal Mejbri",
    "Yassine Bounou":       "Yassine Bounou",
    "Nayef Aguerd":         "Nayef Aguerd",
    "Romain Saiss":         "Romain Saïss",
    "Azzedine Ounahi":      "Azzedine Ounahi",
    "Youssef En-Nesyri":    "Youssef En-Nesyri",
    "Brahim Diaz":          "Brahim Díaz",
    "Edouard Mendy":        "Édouard Mendy",
    "Nicolas Jackson":      "Nicolas Jackson (footballer)",
    "Lamine Camara":        "Lamine Camara (footballer)",
    "Ismaila Sarr":         "Ismaïla Sarr",
    "Iliman Ndiaye":        "Iliman Ndiaye",
    "Krepin Diatta":        "Krepin Diatta",
    "Kalidou Koulibaly":    "Kalidou Koulibaly",
    "Cheikhou Kouyate":     "Cheikhou Kouyaté",
    "Julian Brandt":        "Julian Brandt",
    "Deniz Undav":          "Deniz Undav",
    "Antonio Nusa":         "Antonio Nusa",
    "Mohamed Elyounoussi":  "Mohamed Elyounoussi",
    "Alexander Sorloth":    "Alexander Sørloth",
    "Martin Ødegaard":      "Martin Ødegaard",
    "Sander Berge":         "Sander Berge",
    "Veton Berisha":        "Veton Berisha",
    "Albin Ekdal":          "Albin Ekdal",
    "Anthony Elanga":       "Anthony Elanga",
    "Jesper Karlsson":      "Jesper Karlsson",
    "Kyle Walker":          "Kyle Walker",
    "Trent Alexander-Arnold": "Trent Alexander-Arnold",
    "Declan Rice":          "Declan Rice",
    "Jack Grealish":        "Jack Grealish",
    "Jordan Pickford":      "Jordan Pickford",
    "Luke Shaw":            "Luke Shaw",
    "James Maddison":       "James Maddison",
    "Ollie Watkins":        "Ollie Watkins",
    "Eberechi Eze":         "Eberechi Eze",
    "Marc-Andre ter Stegen": "Marc-André ter Stegen",
    "Antonio Rudiger":      "Antonio Rüdiger",
    "Nico Schlotterbeck":   "Nico Schlotterbeck",
    "Antonio Rudiger":      "Antonio Rüdiger",
    "Moises Caicedo":       "Moisés Caicedo",
    "Pervis Estupinan":     "Pervis Estupiñán",
    "Gonzalo Plata":        "Gonzalo Plata",
    "Enner Valencia":       "Enner Valencia",
    "Miguel Almirón":       "Miguel Almirón",
    "Miguel Almiron":       "Miguel Almirón",
    "Antonio Sanabria":     "Antonio Sanabria",
    "Gustavo Gomez":        "Gustavo Gómez",
    "Julio Enciso":         "Julio Enciso",
    "Mathias Villasanti":   "Mathías Villasanti",
    "Santiago Arzamendia":  "Santiago Arzamendia",
    "Liberato Cacace":      "Liberato Cacace",
    "Chris Wood":           "Chris Wood (footballer)",
    "Ismail Mohamad":       "Ismail Mohamad",
    "Akram Afif":           "Akram Afif",
    "Ali Adnan":            "Ali Adnan",
    "Aymen Hussein":        "Aymen Hussein",
    "Mousa Al-Tamari":      "Mousa Al-Tamari",
    "Oday Dabbagh":         "Oday Dabbagh",
}


RATE_LIMITED = set()  # jugadores que dieron 429, para reintentar al final

def fetch_wiki(name):
    """Usa la API de Wikipedia para obtener el wikitext de un jugador."""
    search_name = NAME_FIXES.get(name, name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote(search_name)}&prop=revisions&rvprop=content&format=json&rvslots=main&redirects=1"
    for attempt in range(4):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if pid == "-1":
                    return ""
                slots = page.get("revisions", [{}])[0].get("slots", {})
                if slots:
                    return slots.get("main", {}).get("*", "")
                return page.get("revisions", [{}])[0].get("*", "")
            return ""
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "Too Many" in err_str:
                wait = 15 * (attempt + 1)
                print(f"\n  [429 rate limit - esperando {wait}s...]  ", end="", flush=True)
                time.sleep(wait)
                RATE_LIMITED.add(name)
            else:
                return ""
    return ""


def parse_wikitext(content):
    """Extrae DOB, altura, peso, club del wikitext."""
    r = {}

    # DOB - múltiples formatos
    # {{Birth date|1987|6|24|df=y}} o {{birth date and age|1987|6|24}}
    m = re.search(r"\{\{[Bb]irth.date[^}]*?\|(\d{4})\|(\d{1,2})\|(\d{1,2})", content)
    if m:
        r["dob"] = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    if "dob" not in r:
        # | birth_date = {{...1987...06...24...}}
        m = re.search(r"birth_date\s*=.*?(\d{4})\D+(\d{1,2})\D+(\d{1,2})", content)
        if m and 1960 < int(m.group(1)) < 2010:
            r["dob"] = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # Altura: | height = {{convert|187|cm|...}} o | height = 1.87 m o | height = 187 cm
    m = re.search(r"\|\s*height\s*=\s*\{\{convert\|(\d+(?:\.\d+)?)\|cm", content)
    if m:
        r["height"] = str(int(float(m.group(1))))
    if "height" not in r:
        m = re.search(r"\|\s*height\s*=\s*(\d+(?:[.,]\d+)?)\s*(?:cm|m)?", content)
        if m:
            val_str = m.group(1).replace(",", ".")
            try:
                val = float(val_str)
                if val < 3:
                    r["height"] = str(int(val * 100))
                elif 140 < val < 230:
                    r["height"] = str(int(val))
            except:
                pass

    # Peso: | weight = {{convert|76|kg|...}} o | weight = 76 kg
    m = re.search(r"\|\s*weight\s*=\s*\{\{convert\|(\d+)\|kg", content)
    if m:
        r["weight"] = m.group(1)
    if "weight" not in r:
        m = re.search(r"\|\s*weight\s*=\s*(\d{2,3})\s*(?:kg)?", content)
        if m:
            val = int(m.group(1))
            if 40 < val < 130:
                r["weight"] = str(val)

    # Club actual - preferir display name en [[Link|Display]]
    m = re.search(r"\|\s*currentclub\s*=\s*([^\n\}\{<]+)", content)
    if m:
        club = m.group(1).strip()
        # [[Page|Display]] → Display, [[Page]] → Page
        club = re.sub(r"\[\[([^\|\]]+)\|([^\]]+)\]\]", r"\2", club)
        club = re.sub(r"\[\[([^\]]+)\]\]", r"\1", club)
        club = re.sub(r"\{\{[^}]*\}\}", "", club).strip()
        club = re.sub(r"<!--.*?-->", "", club).strip()
        club = re.sub(r"\s*\(on loan.*?\)", "", club).strip()
        if club and len(club) > 1:
            r["club"] = club

    if "club" not in r:
        # Buscar en tabla de clubs la última entrada sin año final (club actual)
        # | years = 2023– | clubs = [[Club Name]]
        blocks = re.findall(r"\|\s*years\s*=([^\n]+)\n.*?\|\s*clubs\s*=([^\n]+)", content, re.DOTALL)
        for years, clubs_raw in blocks:
            years_clean = years.strip()
            if re.search(r"\d{4}\s*[–—-]\s*$", years_clean) or re.search(r"\d{4}\s*–?\s*present", years_clean, re.I):
                club = re.sub(r"\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]", r"\1", clubs_raw).strip()
                club = re.sub(r"\{\{[^}]*\}\}", "", club).strip()
                if club and len(club) > 2:
                    r["club"] = club
                    break

    return r


MANUAL_DATA = {
    "Giuliano Simeone": {"dob":"1999-07-07","height":"186","weight":"78","club":"Atlético Madrid"},
    "Franco Mastantuono": {"dob":"2007-03-14","height":"180","weight":"75","club":"Real Madrid"},
    "Nico Paz": {"dob":"2004-01-09","height":"177","weight":"72","club":"Como"},
    "Nico Gonzalez": {"dob":"1997-12-06","height":"182","weight":"79","club":"FC Barcelona"},
}


def get_data(name):
    if name in MANUAL_DATA:
        return MANUAL_DATA[name]
    content = fetch_wiki(name)
    if not content:
        return {}
    return parse_wikitext(content)


def main():
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.csv", encoding="utf-8") as f:
        rows_in = list(csv.DictReader(f))

    # Cargar caché
    cache_path = r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_cache.json"
    try:
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
    except:
        cache = {}

    # Jugadores únicos
    player_names = []
    seen = set()
    for row in rows_in:
        n = row["name"]
        if row["type"] == "player" and n not in seen:
            seen.add(n)
            player_names.append(n)

    total = len(player_names)
    print(f"Total jugadores únicos: {total}")
    print(f"Ya en caché: {sum(1 for p in player_names if p in cache)}")

    for i, name in enumerate(player_names):
        if name in cache:
            continue
        print(f"[{i+1}/{total}] {name}... ", end="", flush=True)
        data = get_data(name)
        # Solo cachear si hay datos reales (no guardar vacíos - se reintentarán)
        if data:
            cache[name] = data
        print(f"DOB:{data.get('dob','?')} H:{data.get('height','?')}cm W:{data.get('weight','?')}kg Club:{data.get('club','?')}", flush=True)
        time.sleep(0.8)
        if i % 10 == 0 and cache:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"\nCaché final: {len(cache)} jugadores")

    # Generar CSV final
    rows_out = []
    for row in rows_in:
        pdata = cache.get(row["name"], {}) or {}
        rows_out.append({
            "team": row["team"], "num": row["num"],
            "name": row["name"], "type": row["type"],
            "dob": pdata.get("dob",""), "height": pdata.get("height",""),
            "weight": pdata.get("weight",""), "club": pdata.get("club",""),
        })

    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_full.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["team","num","name","type","dob","height","weight","club"])
        w.writeheader(); w.writerows(rows_out)
    print("CSV final guardado: stickers_full.csv")

    # Generar JSON para el álbum
    by_team = {}
    for row in rows_out:
        t = row["team"]
        if t not in by_team:
            by_team[t] = {}
        by_team[t][row["num"]] = {
            "name": row["name"], "type": row["type"],
            "dob": row["dob"], "height": row["height"],
            "weight": row["weight"], "club": row["club"],
        }
    with open(r"c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json", "w", encoding="utf-8") as f:
        json.dump(by_team, f, ensure_ascii=False, indent=2)
    print("JSON guardado: players_data.json")


if __name__ == "__main__":
    main()
