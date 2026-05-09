# Album de Simon - Mundial 2026

App web simple (Flask + HTML/CSS/JS) para llevar control de figuritas desde celular Android.

## Que hace hoy

- Registro de figuritas por pais (1..20): la tengo / falta.
- Registro de repetidas por figurita.
- Resumen para copiar o compartir.
- Comparacion con amigo: sugiere que puedes recibir, que puedes dar y canjes mutuos.
- UI mobile-first con controles grandes.

## Requisitos

- Python 3.10+
- Dependencias:

```bash
py -m pip install -r requirements.txt
```

## Ejecutar en PC para usar desde Android (misma Wi-Fi)

1. En Windows, desde la carpeta del proyecto:

```bash
py -m flask --app app run --host 0.0.0.0 --port 5000
```

2. En tu PC, averigua la IP local (ejemplo 192.168.1.35).

3. En Android, abre en el navegador:

```text
http://192.168.1.35:5000
```

## Instalar como app (PWA) en Android

1. Abre la app desde Chrome en Android con la URL local.
2. Si aparece el boton "Instalar app" en la esquina inferior izquierda, tocalo.
3. Si no aparece, abre menu de Chrome y elige "Agregar a pantalla de inicio".
4. Una vez instalada, la app abre en modo standalone (sin barra del navegador).

## Notas de assets

- Si no hay escudos descargados, la app usa `static/img/default-shield.svg` como fallback.
- El scraping de assets es opcional. Puedes usar la app sin scraping.
- El script `scrape_assets.py` ahora usa una estrategia curada:
	- Banderas SVG por pais desde FlagCDN (consistentes y limpias).
	- Logos especiales locales para `FWC` y `CC`.
	- Extra opcional para Argentina desde Wikipedia.
- `CC` usa un logo inspirado con estilo clasico para mejorar legibilidad visual.

## Publicar sin servidor (GitHub Pages)

Esta opcion publica la app estatica de la carpeta `docs/` para abrirla desde cualquier red.

1. Crea un repositorio nuevo en GitHub (vacio).
2. Desde la carpeta del proyecto, ejecuta:

```bash
git init
git add .
git commit -m "App album Simon lista para GitHub Pages"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

3. En GitHub: `Settings` -> `Pages` -> `Build and deployment`:
	- Source: `Deploy from a branch`
	- Branch: `main`
	- Folder: `/docs`

4. Tu link quedara asi:

```text
https://TU_USUARIO.github.io/TU_REPO/
```

## Paleta y estilo (hibrido)

Se aplica un estilo "Argentina + Mundial" inspirado (no claiming de branding oficial exacto):

- Celeste Argentina: `#74ACDF`
- Azul profundo: `#0A3D79`
- Blanco: `#FFFFFF`
- Dorado sol: `#F6B40E`

Fuentes usadas:

- `Montserrat` (titulos)
- `Barlow` (texto y UI)

## Formato para comparar con amigo

En los dos cuadros de texto (faltantes y repetidas), una linea por pais:

```text
ARG: 1,2,3
BRA: 4,10
```

- Codigo de pais en 3 letras (o codigo usado en el album).
- Numeros validos de 1 a 20.
