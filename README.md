# Album Simon - FIFA Mundial 2026

App web offline para rastrear figuritas del álbum Panini del Mundial 2026.

## ✨ Características

- **Sin servidor:** Funciona completamente en el navegador
- **Instalable:** Se puede instalar en Android como app nativa (PWA)
- **Offline:** Funciona sin conexión a internet
- **Grid completa:** Edición masiva de repetidas (50 países × 20 figuritas)
- **Comparación:** Analiza figuritas con amigos para sugerencias de intercambio
- **Compartir:** Botón WhatsApp directo para enviar resumen
- **Backup:** Exportar e importar JSON
- **Miniaturas:** Soporte para imágenes reales con fallback a colores degradados

## 🚀 Instalación Rápida

### Opción A: GitHub Pages (RECOMENDADO - Sin servidor)

Lee el archivo **`GITHUB_PAGES_INSTRUCTIONS.md`** para instrucciones completas paso-a-paso para principiantes.

**Resumen:**
1. Crea un repositorio en GitHub
2. Configura Git en tu PC
3. Sube esta carpeta a `main`
4. Activa GitHub Pages en Settings (rama: main, carpeta: /docs)
5. Accede a: `https://tu-usuario.github.io/album-simon-2026/`

**Ventajas:**
- ✓ Completamente gratis
- ✓ Funciona desde cualquier dispositivo con el link
- ✓ Offline después de cargar
- ✓ Sin necesidad de servidor propio

### Opción B: Local (solo desarrollo)

```bash
# Requiere Python 3.10+
python app.py
# Abre: http://localhost:5000
```

## 📁 Estructura

```
FIGUS MUNDIAL/
├── docs/                          # GitHub Pages (producción)
│   ├── index.html                 # App completa (standalone)
│   ├── manifest.webmanifest       # PWA metadata
│   ├── sw.js                      # Service worker
│   ├── icons/                     # Iconos PWA
│   └── img/stickers/              # Miniaturas (OPCIONAL)
│       ├── ARG-1.jpg
│       ├── ARG-2.jpg
│       └── ...
├── app.py                         # Flask backend (desarrollo)
├── album_simon.json               # Datos JSON (desarrollo)
├── GITHUB_PAGES_INSTRUCTIONS.md   # 📖 Guía para publicar
├── MINIATURAS_INSTRUCCIONES.md    # 📖 Como descargar imágenes
└── README.md                      # Este archivo
```

## 🎨 Colores (Híbrido Argentina + Mundial)

- **Navy:** #0a3d79 (azul profundo)
- **Sky Blue:** #74acdf (celeste argentina)
- **Gold:** #f6b40e (dorado)
- **Gradientes:** Fondo degradado celeste → navy

## 🔧 Tecnología

| Aspecto | Tecnología |
|---------|-----------|
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Storage | localStorage (clave: `album_simon_2026_v3`) |
| PWA | Service Worker + manifest.webmanifest |
| Desarrollo | Flask (Python 3.10+) |
| Hosting | GitHub Pages estático |

## 📊 Contenido

- **50 países** representados
- **20 figuritas** por país = 1000 figuritas totales
- **Faltantes predefinidas** con distribución realista
- **Grid editable:** Tabla 50×20 para edición masiva de repetidas

**Códigos de países:** FWC, MEX, RSA, KOR, CZE, CAN, BIH, QAT, SUI, BRA, MAR, HAI, SCO, USA, PAR, AUS, TUR, GER, COW, CIV, ECU, NED, JPN, SWE, TUN, CC, BEL, EGY, IRN, NZL, ESP, CPV, KSA, URU, FRA, SEN, IRQ, NOR, ARG, ALG, AUT, JOR, POR, COD, UZB, COL, ENG, CRO, GHA, PAN

## 🛠️ Como usar

### 1️⃣ Agregar figuritas

1. Expande un país (ej: Argentina)
2. Marca "La tengo" en la tarjeta
3. Usa los botones +/- para cantidad de repetidas

### 2️⃣ Editar en lote (Grid)

1. Scroll hasta la tabla "Grilla completa de repetidas"
2. Haz clic en cualquier celda para cambiar cantidad
3. Los cambios se sincronizan automáticamente con las tarjetas

### 3️⃣ Comparar con amigos

1. Pega en el primer cuadro: Faltantes del amigo (formato: `ARG: 1,2,3`)
2. Pega en el segundo cuadro: Repetidas del amigo (formato: `BRA: 4,10`)
3. Haz clic en "Comparar" para ver sugerencias
4. Resultado muestra:
   - Lo que tu amigo puede darte
   - Lo que Simon puede darle
   - Canjes mutuos posibles

### 4️⃣ Compartir resumen

Haz clic en "Resumen" y elige:

- **Copiar:** Copia al portapapeles
- **Compartir:** Usa el navegador para compartir
- **WhatsApp:** Abre wa.me con texto codificado para enviar directo

### 5️⃣ Backup & Restaurar

- **Exportar backup:** Descarga JSON con todos tus datos
- **Importar backup:** Sube un JSON previo para recuperar estado

## 📱 En Android (Como PWA)

1. Abre la app en Chrome/navegador
2. Menu → "Instalar app" (o "Agregar a pantalla de inicio")
3. Se instala como app nativa
4. Funciona completamente offline
5. Los datos se guardan en el dispositivo

## 🎞️ Miniaturas (Opcional)

El album funciona 100% sin imágenes (muestra colores degradados). Para agregar miniaturas reales:

Ver archivo **`MINIATURAS_INSTRUCCIONES.md`** que incluye:
- Como descargar desde last-sticker.com
- Extensión recomendada: Image Downloader
- Estructura de carpetas
- Convención de nombres: `{CODIGO}-{NUMERO}.jpg`

**Ejemplos de nombres:**
- `ARG-1.jpg` (Argentina figurita 1)
- `BRA-20.jpg` (Brasil figurita 20)
- `FWC-1.jpg` (Logo Mundial figurita 1)

## 💾 Datos & Privacidad

### Formato de almacenamiento

Los datos se guardan en localStorage del navegador como JSON:

```json
{
  "ARG-1": {"codigo_pais": "ARG", "numero": 1, "la_tengo": true, "repetidas": 0},
  "ARG-2": {"codigo_pais": "ARG", "numero": 2, "la_tengo": false, "repetidas": 3}
}
```

### Privacidad

✓ **Todos los datos se guardan LOCALMENTE** en tu dispositivo  
✓ **No se envía información a servidores** (excepto GitHub Pages para servir archivos)  
✓ **Puedes desconectarte** de internet después de cargar la app  
✓ **Puedes exportar/importar** tus datos en cualquier momento  

## 🐛 Solución de Problemas

### Las imágenes no aparecen
- Verifica que estén en `docs/img/stickers/`
- El nombre debe ser exacto: `ARG-1.jpg` (mayúsculas)
- Recarga la página (Ctrl+F5)
- Abre la consola (F12) y busca errores 404

### El sitio no aparece en GitHub Pages
- Espera 1-2 minutos después de hacer push
- Recarga la página (Ctrl+F5)
- Ve a Settings → Pages y verifica:
  - Branch: main
  - Folder: /docs

### Perdí mis datos
- **Prevención:** Haz backups regularmente (botón "Exportar")
- **Recuperación:** Los datos están en localStorage de tu navegador
- **Cuidado:** Limpiar cookies/cache del navegador borra todo

### El app no funciona offline
- Verifica que el navegador soporte PWA (Chrome, Edge, Firefox)
- Asegúrate de haber abierto la app una vez online
- El service worker se instala automáticamente

## 📚 Recursos útiles

- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **PWA Docs:** https://web.dev/progressive-web-apps/
- **localStorage MDN:** https://developer.mozilla.org/es/docs/Web/API/Window/localStorage
- **Guía GitHub Pages (nuestra):** Leer `GITHUB_PAGES_INSTRUCTIONS.md`

## 🔄 Versiones

| Versión | Tipo | Ubicación | Cuando usar |
|---------|------|-----------|-------------|
| Flask | Desarrollo | `app.py` en local | Testing, cambios de código |
| GitHub Pages | Producción | `docs/index.html` en GitHub | Compartir con otros, usar desde celular |

## 📄 Licencia

Uso personal y educativo. No comercial.

---

**Última actualización:** 2026  
**Versión:** 1.0  
**Estado:** ✅ Producción (GitHub Pages)  
**Soporte:** Sin servidor - completamente offline

**¡A disfrutar del album! 🎉**
