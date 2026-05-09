# Como publicar Album Simon en GitHub Pages - Guía para Principiantes

Esta guía te permite publicar tu álbum de figuritas en internet de forma **gratuita y sin servidor**.

## ¿Qué necesitas?

- Una cuenta de GitHub (crea una en https://github.com si no tienes)
- Git instalado en tu PC (https://git-scm.com/download/win)
- La carpeta de Album Simon con los archivos

---

## PASO 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Escribe un nombre para tu repositorio. Ejemplo: `album-simon-2026`
3. Deja la descripción vacía (opcional)
4. Elige **Public** (así cualquiera con el link puede verlo)
5. Marca la casilla "Add a README file"
6. Haz clic en **Create repository**

**Listo!** GitHub te muestra la URL de tu nuevo repositorio.
Copia esta URL: `https://github.com/TU_USUARIO/album-simon-2026.git`

---

## PASO 2: Configurar Git en tu PC

Abre PowerShell en la carpeta "FIGUS MUNDIAL" y ejecuta estos comandos:

### Paso 2a: Configurar identidad (solo la primera vez)

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@gmail.com"
```

Reemplaza:
- `Tu Nombre` → Tu nombre real
- `tu_email@gmail.com` → El email de tu cuenta GitHub

### Paso 2b: Inicializar Git

```powershell
git init
```

---

## PASO 3: Conectar a GitHub

```powershell
git remote add origin https://github.com/TU_USUARIO/album-simon-2026.git
```

Reemplaza:
- `TU_USUARIO` → Tu usuario de GitHub
- `album-simon-2026` → El nombre que elegiste en Paso 1

**Verifica que funcionó:**
```powershell
git remote -v
```

Debería mostrar dos líneas con `https://github.com/TU_USUARIO/album-simon-2026.git`

---

## PASO 4: Subir los archivos

Ejecuta estos comandos **EN ORDEN**:

```powershell
git add .
```
(Esto prepara todos los archivos)

```powershell
git commit -m "Primera version del album"
```
(Esto guarda una version de tus archivos)

```powershell
git branch -M main
```
(Esto crea la rama principal)

```powershell
git push -u origin main
```
(Esto sube todo a GitHub)

**Si pide usuario/contraseña:**
- Usuario: Tu usuario de GitHub
- Contraseña: Un token de acceso (ver paso especial mas abajo)

---

## ⚠️ IMPORTANTE: Token de acceso si pide contraseña

Si PowerShell pide contraseña, GitHub no acepta la contraseña normal. Necesitas un **token personal**:

1. Ve a https://github.com/settings/tokens
2. Haz clic en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre: `github_pages_token`
4. Marca estas casillas:
   - ✓ repo (completo)
   - ✓ workflow
5. Haz clic en "Generate token"
6. **Copia el token** (aparece una sola vez)
7. En PowerShell, pega el token cuando pida contraseña

---

## PASO 5: Activar GitHub Pages

1. Ve a tu repositorio: `https://github.com/TU_USUARIO/album-simon-2026`
2. Haz clic en **Settings** (engranaje superior derecho)
3. En el menu de la izquierda, haz clic en **Pages**
4. En "Build and deployment":
   - **Source**: Elige "Deploy from a branch"
   - **Branch**: Elige `main` y carpeta `/docs`
5. Haz clic en **Save**

GitHub mostrará un mensaje verde: "Your site is published at:"

---

## PASO 6: Acceder a tu album

Tu album estará disponible en:

```
https://TU_USUARIO.github.io/album-simon-2026/
```

**Cambios:**
- `TU_USUARIO` → Tu usuario de GitHub (ejemplo: juanperez → juanperez.github.io)
- `album-simon-2026` → El nombre del repositorio

**Guarda este link!** Puedes compartirlo con amigos.

---

## ¿Cómo actualizar el album?

Si haces cambios locales y quieres subirlos:

```powershell
git add .
git commit -m "Descripcion del cambio"
git push
```

El album se actualiza automáticamente en 1-2 minutos.

---

## Solución de problemas

### "fatal: not a git repository"
```powershell
git init
git remote add origin https://github.com/TU_USUARIO/album-simon-2026.git
```

### El sitio no aparece después de 5 minutos
1. Espera otro minuto
2. Recarga la página (Ctrl+F5)
3. Verifica Settings → Pages

### Quiero cambiar la URL del repositorio
```powershell
git remote set-url origin https://github.com/TU_USUARIO/nuevo-nombre.git
```

---

## ¡Listo! 🎉

Tu album de figuritas ahora está en internet, completamente gratis y sin necesidad de servidor.

**Comparte el link:** `https://TU_USUARIO.github.io/album-simon-2026/`
