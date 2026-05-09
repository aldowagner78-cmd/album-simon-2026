# Album Simon - Instrucciones para las Miniaturas

## ¿Cómo añadir las imágenes de las figuritas?

El album funciona perfectamente sin imágenes (muestra colores degradados), pero es mucho mejor con las miniaturas reales.

### Opción 1: Descargar desde last-sticker.com (RECOMENDADO)

**Paso 1: Ir a la página de Panini 2026**
1. Abre: https://www.last-sticker.com/cards/panini_world_cup_2026/
2. Deberías ver todas las figuritas del album

**Paso 2: Instalar extensión para descargar imágenes**
1. Descarga la extensión Chrome: "Image Downloader"
   - Ve a: https://chromewebstore.google.com/detail/image-downloader/iijibbppidihbeknagcaeflhegjdhljf
   - Haz clic en "Añadir a Chrome"

**Paso 3: Descargar imágenes**
1. En la página de last-sticker.com, abre la consola de Chrome: Presiona F12
2. Haz clic en la extensión "Image Downloader" (arriba a la derecha)
3. Deberían aparecer todas las imágenes
4. Haz clic en "Download all" para descargar un ZIP

**Paso 4: Extraer y renombrar**
1. Abre el ZIP descargado
2. Busca las imágenes de Panini 2026
3. Copia los archivos JPG de cada figurita a: `docs/img/stickers/`

**Paso 5: Renombrar según el código**

Las imágenes deben tener el nombre: `{CODIGO}-{NUMERO}.jpg`

**Ejemplos:**
- `ARG-1.jpg` (Argentina figurita 1)
- `BRA-20.jpg` (Brasil figurita 20)
- `FWC-1.jpg` (Logo Mundial figurita 1)
- `CC-1.jpg` (Coca-Cola figurita 1)

**Códigos de países:**
```
FWC (Mundial 2026)    | MEX (Mexico)         | RSA (Sudafrica)      | KOR (Corea del Sur)
CZE (Republica Checa) | CAN (Canada)         | BIH (Bosnia)         | QAT (Qatar)
SUI (Suiza)           | BRA (Brasil)         | MAR (Marruecos)      | HAI (Haiti)
SCO (Escocia)         | USA (Estados Unidos) | PAR (Paraguay)       | AUS (Australia)
TUR (Turquia)         | GER (Alemania)       | COW (Costa de Marfil)| CIV (Costa de Marfil)
ECU (Ecuador)         | NED (Paises Bajos)   | JPN (Japon)          | SWE (Suecia)
TUN (Tunez)           | CC (Coca-Cola)       | BEL (Belgica)        | EGY (Egipto)
IRN (Iran)            | NZL (Nueva Zelanda)  | ESP (Espana)         | CPV (Cabo Verde)
KSA (Arabia Saudita)  | URU (Uruguay)        | FRA (Francia)        | SEN (Senegal)
IRQ (Irak)            | NOR (Noruega)        | ARG (Argentina)      | ALG (Argelia)
AUT (Austria)         | JOR (Jordania)       | POR (Portugal)       | COD (R.D. Congo)
UZB (Uzbekistan)      | COL (Colombia)       | ENG (Inglaterra)     | CRO (Croacia)
GHA (Ghana)           | PAN (Panama)
```

### Opción 2: Descargar manualmente

1. Ve a https://www.paninigroup.com/ (sitio oficial)
2. Busca "World Cup 2026"
3. Descarga cada figura individualmente (tedioso pero seguro)
4. Guarda en `docs/img/stickers/` con nombre `{CODIGO}-{NUMERO}.jpg`

## Verificación

Una vez que tengas las imágenes:

1. Abre tu album en el navegador (puede ser local o en GitHub Pages)
2. Expande un país (ej: Argentina)
3. Las figuritas deberían mostrar las miniaturas reales en lugar de colores degradados

Si no aparecen:
- Verifica que el nombre del archivo sea exacto: `ARG-1.jpg` (mayúsculas)
- Verifica que estén en: `docs/img/stickers/`
- Recarga la página (Ctrl+F5)
- Abre la consola (F12) para ver si hay errores

## Alternativa: Solo con colores

El album ya tiene un fallback bonito con colores gradientes para cada país, así que funciona perfectamente sin las miniaturas. ¡No es obligatorio!

---

**Nota:** Si compartes el album por GitHub Pages, cualquiera podrá ver las imágenes que subas. Verifica que sea lo que quieres antes de publicar.
