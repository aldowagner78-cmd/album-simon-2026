"""
Descarga imágenes desde Wikipedia/Wikimedia Commons para el álbum FIFA World Cup 2026.
Escudos + fotos de jugadores. Sin bloqueos (Wikimedia es libre).
Uso: python download_wiki_stickers.py
"""
import requests
import os
import time

OUTPUT_DIR = os.path.join("docs", "img", "stickers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIKI_API = "https://en.wikipedia.org/w/api.php"

# Códigos especiales → artículo del Mundial
SPECIAL_CODES = {
    "FWC": "2026_FIFA_World_Cup",
    "COW": "2026_FIFA_World_Cup",
    "CC":  "2026_FIFA_World_Cup",
}

# Equipos nacionales → artículo de Wikipedia
TEAMS = {
    "MEX": "Mexico_national_football_team",
    "RSA": "South_Africa_national_football_team",
    "KOR": "South_Korea_national_football_team",
    "CZE": "Czech_Republic_national_football_team",
    "CAN": "Canada_national_football_team",
    "BIH": "Bosnia_and_Herzegovina_national_football_team",
    "QAT": "Qatar_national_football_team",
    "SUI": "Switzerland_national_football_team",
    "BRA": "Brazil_national_football_team",
    "MAR": "Morocco_national_football_team",
    "HAI": "Haiti_national_football_team",
    "SCO": "Scotland_national_football_team",
    "USA": "United_States_men%27s_national_soccer_team",
    "PAR": "Paraguay_national_football_team",
    "AUS": "Australia_national_football_team",
    "TUR": "Turkey_national_football_team",
    "GER": "Germany_national_football_team",
    "CIV": "Ivory_Coast_national_football_team",
    "ECU": "Ecuador_national_football_team",
    "NED": "Netherlands_national_football_team",
    "JPN": "Japan_national_football_team",
    "SWE": "Sweden_national_football_team",
    "TUN": "Tunisia_national_football_team",
    "BEL": "Belgium_national_football_team",
    "EGY": "Egypt_national_football_team",
    "IRN": "Iran_national_football_team",
    "NZL": "New_Zealand_national_football_team",
    "ESP": "Spain_national_football_team",
    "CPV": "Cape_Verde_national_football_team",
    "KSA": "Saudi_Arabia_national_football_team",
    "URU": "Uruguay_national_football_team",
    "FRA": "France_national_football_team",
    "SEN": "Senegal_national_football_team",
    "IRQ": "Iraq_national_football_team",
    "NOR": "Norway_national_football_team",
    "ARG": "Argentina_national_football_team",
    "ALG": "Algeria_national_football_team",
    "AUT": "Austria_national_football_team",
    "JOR": "Jordan_national_football_team",
    "POR": "Portugal_national_football_team",
    "COD": "Democratic_Republic_of_the_Congo_national_football_team",
    "UZB": "Uzbekistan_national_football_team",
    "COL": "Colombia_national_football_team",
    "ENG": "England_national_football_team",
    "CRO": "Croatia_national_football_team",
    "GHA": "Ghana_national_football_team",
    "PAN": "Panama_national_football_team",
}

# Palabras que indican imágenes irrelevantes (iconos, banderas, medallas, etc.)
SKIP_WORDS = [
    "flag_of", "flag_", "kit_", "arrow_", "commons-logo", "wikidata",
    "edit", "question_mark", "nuvola", "pictogram", "icon_", "_icon.",
    "symbol_", "blue_pencil", "red_card", "yellow_card", "medal",
    "soccerball", "wiki_letter", "transparentpx", "silhouette",
    "increase", "decrease", "steady", "bronze_", "gold_", "silver_",
    "fibeamer", "globe", "disambig", "portal-", "padlock", "lock",
    "audio", "sound", "video", "map_of", "location_", "relief_",
    "stamp_", "coat_of_arms", "emblem_of_the_united_nations",
]

PLAYERS = {
    "FWC": ["FIFA World Cup","2026 FIFA World Cup","Lionel Messi","Harry Kane","Erling Haaland","Kylian Mbappe","Cristiano Ronaldo","Vinicius Junior","Pedri","Jude Bellingham","Son Heung-min","Neymar","Lamine Yamal","Florian Wirtz","Jamal Musiala"],
    "COW": ["FIFA World Cup","Cristiano Ronaldo","Kylian Mbappe","Neymar","FIFA","Lionel Messi","Harry Kane","Erling Haaland","Mohamed Salah","Kevin De Bruyne","Virgil van Dijk","Joshua Kimmich","Robert Lewandowski","Lamine Yamal","Vinicius Junior"],
    "CC":  ["CONCACAF","Azteca Stadium","MetLife Stadium","FIFA World Cup 2026","SoFi Stadium","AT&T Stadium","Estadio Akron","Levi's Stadium","Lincoln Financial Field","BC Place Stadium","BMO Field","Allegiant Stadium"],
    "MEX": ["Guillermo Ochoa","Hirving Lozano","Raul Jimenez","Edson Alvarez","Santiago Gimenez","Andres Guardado","Hector Herrera","Johan Vasquez","Orbelin Pineda","Cesar Montes","Carlos Vela","Jesus Manuel Corona","Luis Romo","Alexis Vega"],
    "RSA": ["Percy Tau","Ronwen Williams","Themba Zwane","Lyle Foster","Bongani Zungu","Thulani Serero","Itumeleng Khune","Dean Furman","Keagan Dolly","Lebo Mothiba","Siyanda Xulu","Teboho Mokoena","Evidence Makgopa"],
    "KOR": ["Son Heung-min","Lee Kang-in","Kim Min-jae","Hwang Hee-chan","Hwang In-beom","Na Sang-ho","Cho Gue-sung","Kim Young-gwon","Lee Jae-sung","Bae Jun-ho","Kim Seung-gyu","Oh Hyeon-gyu"],
    "CZE": ["Tomas Soucek","Patrik Schick","Vladimir Coufal","Antonin Barak","Jakub Jankto","Ondrej Kolar","Alex Kral","Lukas Masopust","David Zima","Ladislav Krejci","Jan Kuchta","Tomas Holes"],
    "CAN": ["Alphonso Davies","Jonathan David","Cyle Larin","Atiba Hutchinson","Tajon Buchanan","Junior Hoilett","Richie Laryea","Sam Adekugbe","Derek Cornelius","Kamal Miller","Milan Borjan","Stephen Eustaquio","Ismael Kone","Liam Fraser"],
    "BIH": ["Edin Dzeko","Miralem Pjanic","Sead Kolasinac","Amer Gojak","Ermin Bicakcic","Haris Hajradinovic","Ognjen Todorovic","Eldar Civic"],
    "QAT": ["Akram Afif","Almoez Ali","Hassan Al-Haydos","Meshaal Barsham","Bassam Al-Rawi","Assim Madibo","Tariq Salman","Pedro Miguel","Karim Boudiaf"],
    "SUI": ["Granit Xhaka","Xherdan Shaqiri","Manuel Akanji","Yann Sommer","Breel Embolo","Ricardo Rodriguez","Haris Seferovic","Remo Freuler","Silvan Widmer","Fabian Rieder","Noah Okafor","Zeki Amdouni"],
    "BRA": ["Vinicius Junior","Rodrygo","Raphinha","Marquinhos","Alisson Becker","Endrick","Lucas Paqueta","Casemiro","Richarlison","Gabriel Magalhaes","Eder Militao","Danilo","Fred","Gabriel Jesus"],
    "MAR": ["Achraf Hakimi","Hakim Ziyech","Yassine Bounou","Sofyan Amrabat","Azzedine Ounahi","Noussair Mazraoui","Romain Saiss","Youssef En-Nesyri","Selim Amallah","Zakaria Aboukhlal","Ilias Chair"],
    "HAI": ["Duckens Nazon","Wilde-Donald Guerrier","Frantzdy Pierrot","James Lea Siliki","Mickael Cachon","Steeven Saba","Dener","Nicolas Moisan","Kervens Belfort"],
    "SCO": ["Andy Robertson","Scott McTominay","Kieran Tierney","John McGinn","Stuart Armstrong","Ryan Christie","Grant Hanley","Billy Gilmour","Callum McGregor","Ryan Jack","Lyndon Dykes","Craig Gordon"],
    "USA": ["Christian Pulisic","Tyler Adams","Weston McKennie","Giovanni Reyna","Matt Turner","Josh Sargent","Ricardo Pepi","Sergino Dest","Antonee Robinson","Walker Zimmermann","Yunus Musah","Tim Weah","Brenden Aaronson","Jordan Morris"],
    "PAR": ["Miguel Almiron","Antonio Sanabria","Gustavo Gomez","Julio Enciso","Mathias Villasanti","Santiago Arzamendia","Alfredo Aguilar","Fabian Balbuena","Carlos Gonzalez","Jorge Morel","Robert Morales"],
    "AUS": ["Mat Ryan","Mathew Leckie","Martin Boyle","Riley McGree","Aaron Mooy","Ajdin Hrustic","Mitchell Duke","Craig Goodwin","Jamie Maclaren","Brad Smith","Milos Degenek","Nathaniel Atkinson","Garang Kuol","Keanu Baccus"],
    "TUR": ["Arda Guler","Merih Demiral","Hakan Calhanoglu","Cengiz Under","Kenan Yildiz","Ugurcan Cakir","Salih Ozcan","Samet Akaydin","Baris Alper Yilmaz","Ferdi Kadioglu","Zeki Celik","Yunus Akgun"],
    "GER": ["Joshua Kimmich","Jamal Musiala","Florian Wirtz","Kai Havertz","Manuel Neuer","Leroy Sane","Thomas Muller","Leon Goretzka","Antonio Rudiger","Niklas Sule","David Raum","Serge Gnabry","Ilkay Gundogan","Jonas Hofmann"],
    "CIV": ["Sebastien Haller","Franck Kessie","Nicolas Pepe","Simon Adingra","Wilfried Zaha","Max-Alain Gradel","Serge Aurier","Eric Bailly","Ibrahim Sangare","Karim Konate","Jonathan Bamba","Odilon Kossounou"],
    "ECU": ["Enner Valencia","Moises Caicedo","Piero Hincapie","Jeremy Sarmiento","Gonzalo Plata","Felix Torres","Jose Cifuentes","Roberto Arboleda","Pervis Estupinan","Jhegson Mendez","Michael Estrada","Angel Mena"],
    "NED": ["Virgil van Dijk","Frenkie de Jong","Memphis Depay","Cody Gakpo","Xavi Simons","Denzel Dumfries","Nathan Ake","Stefan de Vrij","Tijjani Reijnders","Wout Weghorst","Teun Koopmeiners","Daley Blind","Ryan Gravenberch","Jeremie Frimpong"],
    "JPN": ["Takumi Minamino","Kaoru Mitoma","Daichi Kamada","Wataru Endo","Maya Yoshida","Ritsu Doan","Takehiro Tomiyasu","Hiroki Sakai","Yuto Nagatomo","Keisuke Honda","Ao Tanaka","Junya Ito"],
    "SWE": ["Alexander Isak","Dejan Kulusevski","Emil Forsberg","Victor Lindelof","Anthony Elanga","Robin Olsen","Jens-Lys Cajuste","Mattias Svanberg","Sebastian Larsson","Isak Hien","Zlatan Ibrahimovic","Mikael Lustig"],
    "TUN": ["Youssef Msakni","Wahbi Khazri","Hannibal Mejbri","Ellyes Skhiri","Aissa Laidouni","Dylan Bronn","Ali Maaloul","Seifeddine Jaziri","Montassar Talbi","Naim Sliti","Hamza Rafia","Mohamed Drager"],
    "BEL": ["Kevin De Bruyne","Romelu Lukaku","Thibaut Courtois","Leandro Trossard","Axel Witsel","Toby Alderweireld","Jan Vertonghen","Yannick Carrasco","Dries Mertens","Timothy Castagne","Jeremy Doku","Amadou Onana","Charles De Ketelaere"],
    "EGY": ["Mohamed Salah","Mostafa Mohamed","Omar Marmoush","Mahmoud Trezeguet","Mohamed Elneny","Ahmed Hegazi","Ramadan Sobhi","Amr Warda","Ahmed El-Shenawy","Omar Kamal","Marwan Hamdy"],
    "IRN": ["Mehdi Taremi","Alireza Jahanbakhsh","Sardar Azmoun","Karim Ansarifard","Morteza Pouraliganji","Saman Ghoddos","Ahmad Nourollahi","Ali Gholizadeh","Ehsan Hajsafi","Alireza Beiranvand","Rouzbeh Cheshmi"],
    "NZL": ["Chris Wood","Liberato Cacace","Marco Rojas","Michael Boxall","Ollie Sail","Clayton Lewis","Ryan Thomas","Bill Tuiloma","Joe Bell","Marko Stamenic","Myer Bevan","Matthew Ridenton"],
    "ESP": ["Pedri","Gavi","Dani Olmo","Lamine Yamal","Unai Simon","Nico Williams","Fabian Ruiz","Alejandro Balde","Robin Le Normand","Mikel Oyarzabal","Ferran Torres","Aymeric Laporte","Rodri","Alvaro Morata"],
    "CPV": ["Ryan Mendes","Bebe","Dylan Tavares","Stopira","Steven Fortes","Jeffrey Fortes","Diogo Gomes","Garry Rodrigues","Julio Tavares","Carlos Ponck","Kenny Rocha"],
    "KSA": ["Salem Al-Dawsari","Saleh Al-Shehri","Mohammed Al-Owais","Sami Al-Najei","Mohammed Kanno","Firas Al-Buraikan","Ali Al-Bulaihi","Abdulelah Al-Malki","Abdullah Al-Hamdan","Riyadh Sharahili","Yasser Al-Shahrani"],
    "URU": ["Darwin Nunez","Federico Valverde","Rodrigo Bentancur","Ronald Araujo","Luis Suarez","Edinson Cavani","Giorgian de Arrascaeta","Sebastian Coates","Mathias Olivera","Jose Maria Gimenez","Martin Caceres","Maxi Gomez","Nicolas de la Cruz"],
    "FRA": ["Kylian Mbappe","Antoine Griezmann","Ousmane Dembele","Mike Maignan","Theo Hernandez","William Saliba","Aurelien Tchouameni","Dayot Upamecano","Marcus Thuram","Raphael Varane","Kingsley Coman","Eduardo Camavinga","Adrien Rabiot","Jules Kounde"],
    "SEN": ["Sadio Mane","Edouard Mendy","Kalidou Koulibaly","Iliman Ndiaye","Ismaila Sarr","Pape Gueye","Nampalys Mendy","Bamba Dieng","Nicolas Jackson","Cheikhou Kouyate","Idrissa Gueye","Abdou Diallo"],
    "IRQ": ["Mohanad Ali","Justin Meram","Aymen Hussein","Ali Adnan","Bashar Resan","Ahmed Ibrahim","Amjad Attwan","Saad Natiq","Dhurgham Ismail","Alaa Abbas","Ali Faez"],
    "NOR": ["Erling Haaland","Martin Odegaard","Sander Berge","Alexander Sorloth","Stefan Strandberg","Joshua King","Kristian Thorstvedt","Mohamed Elyounoussi","Ola Solbakken","Patrick Berg","Mathias Normann","Andreas Hanche-Olsen"],
    "ARG": ["Lionel Messi","Angel Di Maria","Rodrigo De Paul","Emiliano Martinez","Julian Alvarez","Lautaro Martinez","Alejandro Garnacho","Enzo Fernandez","Paulo Dybala","German Pezzella","Nicolas Tagliafico","Nahuel Molina","Leandro Paredes"],
    "ALG": ["Riyad Mahrez","Islam Slimani","Sofiane Feghouli","Youcef Belaili","Baghdad Bounedjah","Aissa Mandi","Haris Belkebla","Andy Delort","Samir Nasri","Mohamed Belaili","Said Benrahma","Houssem Aouar"],
    "AUT": ["David Alaba","Marcel Sabitzer","Marko Arnautovic","Konrad Laimer","Michael Gregoritsch","Patrick Wimmer","Florian Kainz","Xaver Schlager","Nicolas Seiwald","Romano Schmid","Stefan Posch","Maximilian Wober"],
    "JOR": ["Musa Al-Taamari","Ahmad Dabbas","Rami Hamada","Baha Faisal","Mousa Suleiman","Ahmad Saleh","Yazan Al-Naimat","Saleh Hardani","Hamza Al-Dardour","Noor Al-Rawabdeh"],
    "POR": ["Cristiano Ronaldo","Bruno Fernandes","Bernardo Silva","Rafael Leao","Ruben Dias","Joao Felix","Diogo Jota","Joao Cancelo","Pepe","Ricardo Horta","Andre Silva","Nuno Mendes","Vitinha","Goncalo Ramos"],
    "COD": ["Yannick Bolasie","Arthur Masuaku","Cedric Bakambu","Chancel Mbemba","Dieumerci Mbokani","Jonathan Bolingi","Britt Assombalonga","Junior Kabananga","Wilfried Zaha","Orel Mangala","Nathan Bakambu"],
    "UZB": ["Eldor Shomurodov","Jaloliddin Masharipov","Ikrom Alibaev","Jamshid Iskanderov","Khojimat Erkinov","Dostonbek Khamdamov","Otabek Shukurov","Sanjar Tursunov","Sherzod Nishonov","Rustam Yusupov"],
    "COL": ["James Rodriguez","Luis Diaz","Falcao","Juan Cuadrado","Davinson Sanchez","Luis Muriel","Roger Martinez","Jefferson Lerma","Camilo Vargas","Daniel Munoz","Richard Rios","Jhon Arias","Miguel Borja","Yerry Mina"],
    "ENG": ["Harry Kane","Jude Bellingham","Declan Rice","Phil Foden","Bukayo Saka","Raheem Sterling","Marcus Rashford","Jordan Pickford","John Stones","Trent Alexander-Arnold","Luke Shaw","Mason Mount","Kalvin Phillips","Jack Grealish"],
    "CRO": ["Luka Modric","Ivan Perisic","Marcelo Brozovic","Mateo Kovacic","Andrej Kramaric","Josko Gvardiol","Nikola Vlasic","Dominik Livakovic","Borna Sosa","Bruno Petkovic","Ante Rebic","Lovro Majer","Dejan Lovren"],
    "GHA": ["Thomas Partey","Jordan Ayew","Andre Ayew","Mohammed Kudus","Joseph Aidoo","Kamaldeen Sulemana","Lawrence Ati-Zigi","Daniel Amartey","Tariq Lamptey","Antoine Semenyo","Inaki Williams","Abdul Fatawu Issahaku"],
    "PAN": ["Roman Torres","Anibal Godoy","Cecilio Waterman","Edgar Barcenas","Alberto Quintero","Jose Luis Rodriguez","Jesus Alfaro","Adalberto Carrasquilla","Ricardo Avila","Freddy Gondola","Omar Browne","Jose Fajardo","Roderick Miller"],
}

session = requests.Session()
session.headers.update({"User-Agent": "AlbumSimon2026/1.0 (student project, non-commercial)"})

def should_skip(title):
    tl = title.lower()
    return any(w in tl for w in SKIP_WORDS)

def wiki_get(params, retries=4):
    """Llamada a la API de Wikipedia con reintentos y respeto de rate limits."""
    for attempt in range(retries):
        try:
            r = session.get(WIKI_API, params=params, timeout=20)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 10 + attempt * 10))
                time.sleep(wait)
                continue
            if r.status_code == 200 and r.text:
                return r.json()
        except Exception:
            pass
        time.sleep(2 + attempt * 2)
    return {}

def get_lead_image_url(article_title, width=350):
    """Retorna la URL del escudo/logo buscando en las imágenes del artículo."""
    # Primero intentar pageimages (imagen principal)
    data = wiki_get({"action": "query", "titles": article_title, "prop": "pageimages", "pithumbsize": str(width), "format": "json"})
    for page in data.get("query", {}).get("pages", {}).values():
        thumb = page.get("thumbnail", {})
        if thumb:
            return thumb.get("source")
    # Si no hay pageimage, buscar logo/badge en las imágenes del artículo
    data2 = wiki_get({"action": "query", "titles": article_title, "prop": "images", "imlimit": "30", "format": "json"})
    candidates = []
    for page in data2.get("query", {}).get("pages", {}).values():
        for img in page.get("images", []):
            t = img["title"].lower()
            if any(w in t for w in ["logo", "badge", "crest", "escudo", "federation", "association"]):
                candidates.append(img["title"])
    if candidates:
        data3 = wiki_get({"action": "query", "titles": "|".join(candidates[:5]), "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": str(width), "format": "json"})
        best_url, best_size = None, 0
        for page in data3.get("query", {}).get("pages", {}).values():
            for info in page.get("imageinfo", []):
                url = info.get("thumburl") or info.get("url", "")
                size = info.get("size", 0)
                if url and size > best_size:
                    best_url, best_size = url, size
        if best_url:
            return best_url
    return None

def get_player_image_url(name, width=350):
    """Busca foto de un jugador: primero por título directo, luego por búsqueda."""
    # Intento 1: título directo
    data = wiki_get({"action": "query", "titles": name.replace(" ", "_"), "prop": "pageimages", "pithumbsize": str(width), "format": "json"})
    for page in data.get("query", {}).get("pages", {}).values():
        if "missing" not in page:
            thumb = page.get("thumbnail", {})
            if thumb:
                return thumb.get("source")
    # Intento 2: búsqueda (maneja acentos, homónimos, etc.)
    data2 = wiki_get({"action": "query", "generator": "search", "gsrsearch": name + " footballer", "gsrlimit": "1", "prop": "pageimages", "pithumbsize": str(width), "format": "json"})
    for page in data2.get("query", {}).get("pages", {}).values():
        thumb = page.get("thumbnail", {})
        if thumb:
            return thumb.get("source")
    return None

def get_article_images(article_title):
    """Retorna lista de títulos de imágenes del artículo (filtrados)."""
    data = wiki_get({"action": "query", "titles": article_title, "prop": "images", "imlimit": "50", "format": "json"})
    result = []
    for page in data.get("query", {}).get("pages", {}).values():
        for img in page.get("images", []):
            t = img["title"]
            if not should_skip(t):
                result.append(t)
    return result

def get_image_urls_batch(file_titles, width=350):
    """Retorna dict {title: url} para un lote de hasta 50 imágenes."""
    if not file_titles:
        return {}
    data = wiki_get({"action": "query", "titles": "|".join(file_titles[:50]), "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": str(width), "format": "json"})
    urls = {}
    for page in data.get("query", {}).get("pages", {}).values():
        title = page.get("title", "")
        for info in page.get("imageinfo", []):
            url = info.get("thumburl") or info.get("url", "")
            size = info.get("size", 0)
            if url and size > 3000:
                urls[title] = url
    return urls

def download_for_country(code, article):
    downloaded = 0

    # Sticker 1: escudo del equipo (pageimages del artículo)
    p1 = os.path.join(OUTPUT_DIR, f"{code}-1.jpg")
    if os.path.exists(p1) and os.path.getsize(p1) > 1000:
        downloaded += 1
    else:
        url = get_lead_image_url(article)
        if url and save_image(url, p1):
            downloaded += 1
            time.sleep(0.1)

    # Stickers 2+: fotos de jugadores conocidos
    for player in PLAYERS.get(code, []):
        if downloaded >= 20:
            break
        n = downloaded + 1
        fp = os.path.join(OUTPUT_DIR, f"{code}-{n}.jpg")
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            downloaded += 1
            continue
        url = get_player_image_url(player)
        if url and save_image(url, fp):
            downloaded += 1
        time.sleep(0.12)

    # Rellenar huecos con imágenes del artículo
    if downloaded < 20:
        imgs = get_article_images(article)
        url_map = get_image_urls_batch(imgs)
        for _, url in url_map.items():
            if downloaded >= 20:
                break
            n = downloaded + 1
            fp = os.path.join(OUTPUT_DIR, f"{code}-{n}.jpg")
            if os.path.exists(fp) and os.path.getsize(fp) > 1000:
                downloaded += 1
                continue
            if save_image(url, fp):
                downloaded += 1
            time.sleep(0.08)

    return downloaded

def save_image(url, filepath):
    """Descarga y guarda una imagen. Retorna True si éxito."""
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200 and len(r.content) > 3000:
            with open(filepath, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False


# ============ MAIN ============
print("=" * 50)
print("  Descarga de imágenes desde Wikipedia")
print("  Album FIFA World Cup 2026 - Simón")
print("=" * 50)
print()

# Test de conexión
print("Probando acceso a Wikipedia...", end=" ", flush=True)
try:
    test = session.get(WIKI_API, params={
        "action": "query", "titles": "FIFA_World_Cup", "format": "json"
    }, timeout=10)
    if test.status_code == 200:
        print("OK!")
    else:
        print(f"ERROR (status {test.status_code})")
        exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

print()
total_ok = 0

# Categorías especiales + equipos nacionales (todos en PLAYERS)
ALL_CODES = list(SPECIAL_CODES.keys()) + list(TEAMS.keys())
ALL_ARTICLES = {**SPECIAL_CODES, **TEAMS}

for code in ALL_CODES:
    article = ALL_ARTICLES[code]
    print(f"{code:4s} ... ", end="", flush=True)
    n = download_for_country(code, article)
    total_ok += n
    status = "OK" if n >= 10 else ("PARCIAL" if n > 0 else "SIN IMGS")
    print(f"{n}/20  [{status}]")
    time.sleep(0.8)

print()
print("=" * 50)
print(f"  COMPLETADO: {total_ok} imágenes descargadas")
print(f"  Carpeta: {os.path.abspath(OUTPUT_DIR)}")
print("=" * 50)
