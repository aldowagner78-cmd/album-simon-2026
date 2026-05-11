import re

AI_DATA = """ALG|12|Nabil Bentalab|1994-11-24|187|LOSC Lille|Centrocampista
ALG|14|Farés Chaibi|2002-11-28|183|Eintracht Frankfurt|Centrocampista
ALG|20|Mohammed Amoura|2000-05-09|170|VfL Wolfsburg|Delantero
ARG|2|Emiliano Martinez|1992-09-02|195|Aston Villa|Portero
AUS|9|Lewis Miller|2000-08-24|187|Hibernian|Defensa
AUS|18|Kusini Vengi|1999-01-15|190|Cerezo Osaka|Delantero
AUS|20|Mohamed Touré|2004-03-26|184|Randers FC|Delantero
BIH|3|Amer Dedic|2002-08-18|180|Red Bull Salzburg|Defensa
BIH|6|Nihad Mujakic|1998-04-15|189|Gaziantep FK|Defensa
BIH|12|Ivan Basic|2002-04-30|176|Orenburg|Centrocampista
BRA|3|Bento|1999-06-10|190|Al-Nassr|Portero
BRA|4|Marquinhos|1994-05-14|183|Paris Saint-Germain|Defensa
BRA|7|Danilo|1991-07-15|184|Juventus|Defensa
BRA|8|Wesley|2003-09-06|170|Flamengo|Defensa
BRA|12|Luiz Henrique|2001-01-02|182|Botafogo|Delantero
BRA|16|João Pedro|2001-09-26|182|Brighton & Hove Albion|Delantero
BRA|20|Estévão|2007-04-24|176|Chelsea|Delantero
CAN|2|Dayne St.Clair|1997-05-09|190|Minnesota United FC|Portero
CAN|6|Riche Larvea|1995-01-07|175|Toronto FC|Defensa
CIV|12|Ibrahim Sangare|1997-12-02|191|Nottingham Forest|Centrocampista
COL|6|Daniel Munoz|1996-05-26|181|Crystal Palace|Defensa
COL|17|Jon Arias|1997-09-21|170|Fluminense|Centrocampista
COL|18|Jhon Cordova|1993-05-11|188|Krasnodar|Delantero
COL|20|Luis Diaz|1997-01-13|180|Liverpool|Delantero
COW|12|Ibrahim Sangare|1997-12-02|191|Nottingham Forest|Centrocampista
CPV|4|Pico|1992-06-17|185|Shamrock Rovers|Defensa
CPV|5|Diney|1995-01-17|190|Al Bataeh|Defensa
CPV|8|Joao Paulo|1998-05-26|178|Sheriff Tiraspol|Centrocampista
CPV|10|Kevin Pina|1997-01-27|181|Krasnodar|Centrocampista
CPV|20|Bebe|1990-07-12|190|Rayo Vallecano|Delantero
CZE|3|Jindrich Stanek|1996-04-27|192|Slavia Praha|Portero
CZE|4|Ladislav Krejci|1999-04-20|191|Wolverhampton|Defensa
CZE|16|Vasil Kusej|2000-05-24|168|Mladá Boleslav|Delantero
CZE|18|Vaclav Cerny|1997-10-17|182|Rangers|Delantero
ECU|10|Alan Franco|1998-08-21|175|Atlético Mineiro|Centrocampista
ECU|14|John Veboah|2000-06-23|170|Venezia|Delantero
ECU|19|Kevin Rodriguez|2000-03-04|190|Union SG|Delantero
EGY|4|Mohamed Hamdy|1995-03-15|176|Pyramids FC|Defensa
EGY|14|Mohamed Lasheen|1996-05-29|174|Pyramids FC|Centrocampista
EGY|18|Mostafa Mohamed|1997-11-28|185|FC Nantes|Delantero
EGY|19|Trezeguet|1994-10-01|179|Al-Rayyan|Delantero
ENG|15|Anthony Gordon|2001-02-24|183|Newcastle United|Delantero
ESP|10|Rodri|1996-06-22|191|Manchester City|Centrocampista
ESP|17|Nico Williams|2002-07-12|181|Athletic Club|Delantero
GHA|7|Gideon Mensah|1998-07-18|178|AJ Auxerre|Defensa
GHA|9|Abdul Issahaku Fatawu|2004-03-08|177|Leicester City|Delantero
GHA|17|Andrew Ayew|1989-12-17|176|Le Havre|Delantero
HAI|15|Derrick Etienne Jr|1996-11-25|175|Toronto FC|Centrocampista
IRN|11|Saeed Ezatolahi|1996-10-01|190|Shabab Al-Ahli|Centrocampista
IRQ|4|Hussein Ali|2002-03-01|175|SC Heerenveen|Defensa
IRQ|5|Akam Hashem|1998-08-16|183|Erbil SC|Defensa
IRQ|11|Ibrahim Bavesh|2000-05-01|175|Al-Quwa Al-Jawiya|Centrocampista
JOR|7|Saleem Obaid|1992-01-17|180|Al-Hussein SC|Defensa
JOR|9|Ibrahim Saadeh|2000-04-27|176|Al-Khor|Centrocampista
JPN|19|Koki Ogawa|1997-08-08|186|NEC Nijmegen|Delantero
KOR|2|Hyeon-woo Jo|1991-09-25|189|Ulsan HD|Portero
KOR|3|Seung-Gyu Kim|1990-09-30|187|Al-Shabab|Portero
KOR|4|Min-jae Kim|1996-11-15|190|Bayern München|Defensa
KOR|5|Yu-min Cho|1996-11-17|182|Sharjah FC|Defensa
KOR|6|Young-woo Seol|1998-12-05|180|Crvena Zvezda|Defensa
KOR|7|Han-beom Lee|2002-06-17|190|FC Midtjylland|Defensa
KOR|8|Tae-seok Lee|2002-07-28|173|FC Seoul|Defensa
KOR|9|Myung-jae Lee|1993-11-04|180|Ulsan HD|Defensa
KOR|10|Jae-sung Lee|1992-08-10|180|1. FSV Mainz 05|Centrocampista
KOR|11|In-beom Hwang|1996-09-20|177|Feyenoord|Centrocampista
KOR|14|Seung-ho Paik|1997-03-17|173|Birmingham City|Centrocampista
KOR|16|Dongg-yeong Lee|1997-09-20|175|Gimcheon Sangmu|Centrocampista
KOR|17|Gue-sung Cho|1998-01-25|189|FC Midtjylland|Delantero
KOR|20|Hyeon-Gyu Oh|2001-04-12|185|Genk|Delantero
KSA|2|Nawaf Alaqidi|2000-05-10|189|Al-Nassr|Portero
KSA|5|Nawaf Bouwashl|1999-09-16|173|Al-Nassr|Defensa
KSA|6|Jihad Thakri|?|?|?|?
KSA|8|Hassan Altambakti|1999-02-09|182|Al-Hilal|Defensa
KSA|9|Musab Aljuwayr|2003-06-20|175|Al-Shabab|Centrocampista
KSA|10|Ziyad Aljohani|2001-11-11|176|Al-Ahli|Centrocampista
KSA|11|Abdullah Alkhaibari|1996-08-16|175|Al-Nassr|Centrocampista
KSA|12|Nasser Aldawsari|1998-12-19|177|Al-Hilal|Centrocampista
KSA|14|Saleh Abu Alshamat|2002-08-11|175|Al-Taawoun|Defensa
KSA|15|Marwan Alsahafi|2004-02-17|175|Beerschot|Centrocampista
KSA|16|Salem Aldawsari|1991-08-19|171|Al-Hilal|Centrocampista
KSA|18|Feras Akbrikan|2000-05-14|181|Al-Ahli|Delantero
MAR|3|Munir El Kajoui|1989-05-10|190|RS Berkane|Portero
MAR|7|Roman Saiss|1990-03-26|190|Al-Shabab|Defensa
MAR|8|Jawad El Yamio|1992-03-29|193|Al-Wehda|Defensa
MEX|3|Johan Vasquez|1998-10-22|184|Genoa|Defensa
MEX|4|Jorge Sánchez|1997-12-10|175|Cruz Azul|Defensa
MEX|9|Carlos Rodriguez|1997-01-03|171|Cruz Azul|Centrocampista
MEX|12|Marcel Ruiz|2000-10-26|179|Toluca|Centrocampista
MEX|18|Alexis Vega|1997-11-25|173|Toluca|Delantero
MEX|20|Cesar Huerta|2000-12-03|171|Pumas UNAM|Delantero
NOR|4|Leo Ostigård|1999-11-28|182|Rennes|Defensa
NZL|2|Max Crocombe Payne|1993-08-12|194|Burton Albion|Portero
NZL|6|Tim Payne|1994-01-10|180|Wellington Phoenix|Defensa
NZL|10|Joe Bell|1999-04-27|182|Viking FK|Centrocampista
NZL|17|Chris Wood|1991-12-07|191|Nottingham Forest|Delantero
PAN|5|Andres Andrade|1998-10-16|187|LASK|Defensa
PAN|7|Eric Davis|1991-03-31|177|Vila Nova|Defensa
PAN|8|Jose Cordoba|2001-06-03|187|Norwich City|Defensa
PAN|10|Cristian Martinez|1997-02-06|178|Al Jandal|Centrocampista
PAN|16|Ismael Díaz|1997-05-12|180|Universidad Católica|Delantero
PAN|17|Jose Fajardo|1993-08-18|182|Universidad Católica|Delantero
PAN|19|Jose Luiz Rodriguez|1998-06-19|180|Red Star Belgrade|Delantero
PAN|20|Alberto Quintero|1987-12-18|165|Plaza Amador|Centrocampista
PAR|2|Roberto Fernandez|2000-06-07|188|Dynamo Moscow|Defensa
PAR|10|Diego Gomez|2003-03-27|184|Inter Miami|Centrocampista
PAR|12|Andres Cubas|1996-05-22|166|Vancouver Whitecaps|Centrocampista
PAR|14|Matias Galarza Fonda|2002-02-11|183|Talleres|Centrocampista
PAR|15|Julio Enciso|2004-01-23|173|Brighton & Hove Albion|Delantero
PAR|18|Ramon Sosa|1999-08-31|178|Nottingham Forest|Delantero
PAR|19|Angel Romero|1992-07-04|176|Corinthians|Delantero
POR|7|Nuno Mendes|2002-06-19|176|Paris Saint-Germain|Defensa
POR|10|Bruno Fernandes|1994-09-08|179|Manchester United|Centrocampista
POR|12|Vitinha|2000-02-13|172|Paris Saint-Germain|Centrocampista
QAT|3|Sultan Albrake|1996-04-07|175|Al-Duhail|Defensa
QAT|4|Lucas Mendes|1990-07-03|184|Al-Wakrah|Defensa
QAT|7|Pedro Miguel|1990-08-06|188|Al-Sadd|Defensa
QAT|9|Mohamed Al-Mannai|2003-10-30|189|Al-Shamal|Centrocampista
QAT|18|Akram Hassan Afif|1996-11-18|177|Al-Sadd|Delantero
RSA|11|Teboho Mokoena|1997-01-24|176|Mamelodi Sundowns|Centrocampista
RSA|14|Bathasi Aubaas|1995-05-14|180|Mamelodi Sundowns|Centrocampista
SCO|3|Jack Hendry|1995-05-07|192|Al-Ettifaq|Defensa
SEN|5|Abdoulaye Seck|1992-06-04|192|Maccabi Haifa|Defensa
SEN|14|Lamine Camara|2004-01-01|173|AS Monaco|Centrocampista
SEN|19|Nicolas Jackson|2001-06-20|188|Chelsea|Delantero
SUI|5|Ricardo Rodriguez|1992-08-25|180|Real Betis|Defensa
SWE|5|Emil Holm|2000-05-13|191|Bologna|Defensa
SWE|7|Gustaf Lagerbielke|2000-04-10|191|FC Twente|Defensa
SWE|9|Hugo Larsson|2004-06-27|187|Eintracht Frankfurt|Centrocampista
TUN|7|Ali Abdi|1993-12-20|183|OGC Nice|Defensa
TUR|18|Baris Alper Yilmaz|2000-05-23|186|Galatasaray|Delantero
URU|6|Sebastian Caceres|1999-08-18|180|Club América|Defensa
URU|7|Mathias Olivera|1997-10-31|184|Napoli|Defensa
URU|14|Manuel Ugarte|2001-04-11|182|Manchester United|Centrocampista
URU|16|Maxi Araujo|2000-02-15|179|Sporting CP|Centrocampista
USA|2|Math Freese|1998-09-02|191|New York City FC|Portero
USA|3|Chris Richards|2000-03-28|188|Crystal Palace|Defensa
USA|5|Mark McKenzie|1999-02-25|183|Toulouse|Defensa
USA|8|Tyler Adams|1999-02-14|175|AFC Bournemouth|Centrocampista
USA|10|Weston McKenny|1998-08-28|185|Juventus|Centrocampista
USA|11|Christian Roldan|1995-06-05|173|Seattle Sounders FC|Centrocampista
UZB|3|Farrukh Savfiev|1991-01-17|176|Navbahor|Defensa"""

# Parse data
updates = {}
incomplete = []

for line in AI_DATA.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    parts = line.split('|')
    if len(parts) != 7:
        print(f"FORMATO INCORRECTO: {line}")
        continue
    country, num, name, dob, height, club, pos = [p.strip() for p in parts]
    num = int(num)
    entry = {
        'dob':    None if dob    == '?' else dob,
        'height': None if height == '?' else int(height),
        'club':   None if club   == '?' else club,
        'pos':    None if pos    == '?' else pos,
        'name':   name,
    }
    updates[(country, num)] = entry
    missing_fields = [f for f, v in [('dob', entry['dob']), ('height', entry['height']),
                                      ('club', entry['club']), ('pos', entry['pos'])] if v is None]
    if missing_fields:
        incomplete.append((country, num, name, missing_fields))

print(f"Datos parseados: {len(updates)} jugadores")
print(f"Con campos faltantes (?): {len(incomplete)}")
for c, n, name, fields in incomplete:
    print(f"  {c}|{n}|{name}: faltan {fields}")
print()

# Read HTML
with open('docs/index.html', encoding='utf-8') as f:
    html = f.read()

# Find PLAYERS block boundaries
start_marker = 'const PLAYERS = {'
start_idx = html.index(start_marker) + len(start_marker) - 1  # points to opening {

# Find matching closing brace
depth = 0
end_idx = start_idx
for i, ch in enumerate(html[start_idx:], start_idx):
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            end_idx = i
            break

players_block = html[start_idx:end_idx + 1]
modified_block = players_block

updated_count = 0
not_found = []

for (country, num), data in sorted(updates.items()):
    # Find the country section: "COUNTRY":{
    country_start = modified_block.find(f'"{country}"{{')   # finds "ALG"{  — NO colon variant
    if country_start == -1:
        country_start = modified_block.find(f'"{country}":{{')  # finds "ALG":{
    if country_start == -1:
        not_found.append(f"{country}|{num} (country block not found)")
        continue

    # Find start of country block (the { after the colon)
    cb_open = modified_block.index('{', country_start + len(f'"{country}"'))

    # Find end of country block by matching braces
    depth = 0
    cb_close = cb_open
    for i, ch in enumerate(modified_block[cb_open:], cb_open):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                cb_close = i
                break

    country_section = modified_block[cb_open:cb_close + 1]

    # Find player entry by number: NUM:{...}  (single-level braces only)
    entry_pattern = re.compile(rf'(?<!\d){num}:\{{([^{{}}]+)\}}')
    m = entry_pattern.search(country_section)
    if not m:
        not_found.append(f"{country}|{num} (entry not found in country block)")
        continue

    old_entry_str = m.group(0)
    old_inner = m.group(1)

    # Extract existing name (use name from file, not from AI)
    name_m = re.search(r'n:"([^"]+)"', old_inner)
    existing_name = name_m.group(1) if name_m else data['name']

    # Build new inner - always start fresh
    new_inner = f'n:"{existing_name}",t:"J"'
    if data['dob']:    new_inner += f',d:"{data["dob"]}"'
    if data['height']: new_inner += f',h:"{data["height"]}"'
    if data['club']:   new_inner += f',c:"{data["club"]}"'
    if data['pos']:    new_inner += f',p:"{data["pos"]}"'

    new_entry_str = f'{num}:{{{new_inner}}}'

    new_country_section = country_section.replace(old_entry_str, new_entry_str, 1)
    modified_block = modified_block[:cb_open] + new_country_section + modified_block[cb_close + 1:]
    updated_count += 1

# Replace PLAYERS block in HTML
new_html = html[:start_idx] + modified_block + html[end_idx + 1:]

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✅ Jugadores actualizados en index.html: {updated_count}")

if not_found:
    print(f"\n⚠️  No encontrados ({len(not_found)}):")
    for x in not_found:
        print(f"  {x}")

print()
print("=" * 60)
print(f"JUGADORES CON DATOS INCOMPLETOS: {len(incomplete)}")
for c, n, name, fields in incomplete:
    print(f"  {c}|{n}|{name}: faltan {fields}")
