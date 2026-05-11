"""
Genera players_data.json combinando stickers_scanini.json + players_cache.json
"""
import json, re, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

with open(r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_cache.json', encoding='utf-8') as f:
    cache = json.load(f)

with open(r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\stickers_scanini.json', encoding='utf-8') as f:
    stickers = json.load(f)

def clean_club(club):
    if not club:
        return ''
    # [[Club Name|Display]] -> Display o Club Name
    club = re.sub(r'\[\[([^\|\]]+)\|([^\]]+)\]\]', r'\2', club)
    # [[Club Name]] -> Club Name
    club = re.sub(r'\[\[([^\]]+)\]\]', r'\1', club)
    # [[Club Name sin cerrar -> Club Name
    club = re.sub(r'\[\[(.+)', r'\1', club)
    club = re.sub(r'\{\{[^}]*\}\}', '', club)
    club = re.sub(r'<!--.*?-->', '', club)
    club = re.sub(r'\s*\(on loan from[^)]+\)', '', club, flags=re.I)
    club = re.sub(r'\s*\([^)]+\)\s*$', '', club)  # quitar "(country)" al final
    return club.strip()

by_team = {}
total_with_data = 0

for team_code, sticker_dict in stickers.items():
    teams_to_fill = [team_code]
    if team_code == 'CIV':
        teams_to_fill = ['CIV', 'COW']  # mismo equipo, dos códigos en el app
    if team_code == 'CUW':
        continue  # no está en el app

    for tcode in teams_to_fill:
        if tcode not in by_team:
            by_team[tcode] = {}
        for num_str, sdata in sticker_dict.items():
            name = sdata.get('name', '')
            stype = sdata.get('type', '')
            pdata = cache.get(name, {}) or {}
            club = clean_club(pdata.get('club', ''))
            if pdata.get('dob') or pdata.get('height') or club:
                total_with_data += 1
            by_team[tcode][num_str] = {
                'name': name,
                'type': stype,
                'dob': pdata.get('dob', ''),
                'height': pdata.get('height', ''),
                'weight': pdata.get('weight', ''),
                'club': club,
            }

print(f'Equipos: {len(by_team)}')
print(f'Stickers con datos bio: {total_with_data}')
print()
print('ARG sample:')
arg = by_team.get('ARG', {})
for n in ['1', '2', '13', '17', '20']:
    print(f'  [{n}] {arg.get(n, {})}')

with open(r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\players_data.json', 'w', encoding='utf-8') as f:
    json.dump(by_team, f, ensure_ascii=False, indent=2)
print()
print('players_data.json guardado!')
