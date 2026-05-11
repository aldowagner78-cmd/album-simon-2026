import os, json

with open('stickers_scanini.json', encoding='utf-8') as f:
    scanini = json.load(f)

OUT = 'docs/img/stickers'
COUNTRIES = ['FWC','MEX','RSA','KOR','CZE','CAN','BIH','QAT','SUI','BRA','MAR','HAI','SCO','USA','PAR','AUS','TUR','GER','COW','CIV','ECU','NED','JPN','SWE','TUN','CC','BEL','EGY','IRN','NZL','ESP','CPV','KSA','URU','FRA','SEN','IRQ','NOR','ARG','ALG','AUT','JOR','POR','COD','UZB','COL','ENG','CRO','GHA','PAN']

need = have = missing = 0
for team in COUNTRIES:
    team_data = scanini.get(team, {})
    for num_str, s in team_data.items():
        t = s.get('type', '')
        if 'logo' in t or 'photo' in t or 'special' in t:
            continue
        need += 1
        path = os.path.join(OUT, f'{team}-{num_str}.jpg')
        if os.path.exists(path):
            have += 1
        else:
            missing += 1

print(f'Fotos jugadores necesarias: {need}')
print(f'Con archivo (puede ser imagen incorrecta): {have}')
print(f'Sin archivo: {missing}')

# ARG ejemplo
print('\nARG - archivos existentes vs Scanini:')
for num_str, s in sorted(scanini['ARG'].items(), key=lambda x: int(x[0])):
    t = s.get('type', '')
    if 'logo' in t or 'photo' in t:
        continue
    path = os.path.join(OUT, 'ARG-' + num_str + '.jpg')
    exists = os.path.exists(path)
    name = s.get('name', '')
    print(f'  ARG-{num_str}: {name} -> {"SI" if exists else "NO"}')
