import re

with open('docs/index.html', encoding='utf-8') as f:
    html = f.read()

tests = [('ALG', 12), ('BRA', 4), ('KOR', 4), ('ESP', 10), ('KSA', 6), ('POR', 10), ('URU', 14)]
idx = html.index('const PLAYERS = {')

for country, num in tests:
    ci = html.find(f'"{country}"', idx)
    if ci == -1:
        print(f'{country}|{num}: PAIS NO ENCONTRADO')
        continue
    cb = html.index('{', ci)
    snippet = html[cb:cb + 3000]
    em = re.search(rf'(?<!\d){num}:\{{([^}}]+)\}}', snippet)
    if em:
        print(f'{country}|{num}: {em.group(1)[:100]}')
    else:
        print(f'{country}|{num}: ENTRADA NO ENCONTRADA')

# Count total players with p field
p_count = len(re.findall(r',p:"[^"]+"', html))
d_count = len(re.findall(r',d:"[^"]+"', html))
print(f'\nTotal entradas con posicion (p): {p_count}')
print(f'Total entradas con fecha (d): {d_count}')
