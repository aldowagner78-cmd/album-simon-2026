import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

with open(r'c:\Users\usuario\Desktop\FIGUS MUNDIAL\docs\index.html', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('APP_VERSION 15', '2026.05.09.15' in html),
    ('PLAYERS bloque', 'const PLAYERS = {' in html),
    ('ARG sticker 17 Messi', 'Lionel Messi' in html),
    ('sticker-club CSS', 'sticker-club' in html),
    ('sticker-bio HTML', 'sticker-bio' in html),
    ('sClub variable', 'const sClub' in html),
    ('sDob variable', 'const sDob' in html),
    ('overflow hidden CSS', 'overflow: hidden' in html),
]
for name, ok in checks:
    print(f'  {"OK" if ok else "FALLO"} {name}')

# Mostrar template de tarjeta
idx = html.find('const pd = ')
if idx >= 0:
    block = html[idx:idx+900]
    print()
    print('Template:')
    print(block)
else:
    print('FALLO: const pd no encontrado')
