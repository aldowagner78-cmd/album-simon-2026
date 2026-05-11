"""
Descarga las 1000 figuritas de laststicker.com usando Playwright (Chrome real)
Uso: python download_stickers.py
"""
import asyncio
import base64
import os
from playwright.async_api import async_playwright

ALBUM_ID = 12176
OUTPUT_DIR = os.path.join("docs", "img", "stickers")

CODES = [
    "fwc","mex","rsa","kor","cze","can","bih","qat","sui","bra",
    "mar","hai","sco","usa","par","aus","tur","ger","cow","civ",
    "ecu","ned","jpn","swe","tun","cc","bel","egy","irn","nzl",
    "esp","cpv","ksa","uru","fra","sen","irq","nor","arg","alg",
    "aut","jor","por","cod","uzb","col","eng","cro","gha","pan"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Visitar el sitio primero para obtener cookies de Cloudflare
        print("Iniciando sesion en laststicker.com ...")
        await page.goto("https://www.laststicker.com/cards/panini_world_cup_2026/ned6/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Probar descarga
        print("Probando descarga de ned6.jpg ...")
        test = await page.evaluate("""async () => {
            const r = await fetch('https://www.laststicker.com/i/cards/12176/ned6.jpg', {credentials: 'include'});
            return {status: r.status, size: (await r.arrayBuffer()).byteLength};
        }""")
        print(f"Status: {test['status']} - Size: {test['size']} bytes")

        if test['status'] != 200:
            print("ERROR: No se pudo descargar. Saliendo.")
            await browser.close()
            return

        print(f"OK! Descargando {len(CODES) * 20} figuritas...\n")

        ok = 0
        fail = 0
        failed_list = []

        for code in CODES:
            country_ok = 0
            for n in range(1, 21):
                filename = f"{code.upper()}-{n}.jpg"
                filepath = os.path.join(OUTPUT_DIR, filename)

                if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                    ok += 1
                    country_ok += 1
                    continue

                url = f"https://www.laststicker.com/i/cards/{ALBUM_ID}/{code}{n}.jpg"
                try:
                    result = await page.evaluate(f"""async () => {{
                        const r = await fetch('{url}', {{credentials: 'include'}});
                        if (r.status !== 200) return {{ok: false, status: r.status}};
                        const buf = await r.arrayBuffer();
                        const bytes = new Uint8Array(buf);
                        let bin = '';
                        for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
                        return {{ok: true, b64: btoa(bin), size: bytes.length}};
                    }}""")

                    if result.get('ok') and result.get('size', 0) > 1000:
                        data = base64.b64decode(result['b64'])
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        ok += 1
                        country_ok += 1
                    else:
                        fail += 1
                        failed_list.append(f"{code}{n}")
                except Exception as e:
                    fail += 1
                    failed_list.append(f"{code}{n}")

                await page.wait_for_timeout(60)

            print(f"{code.upper():4s}: {country_ok}/20   [OK={ok} FAIL={fail}]")

        await browser.close()

        print(f"\n{'='*40}")
        if fail == 0:
            print(f"COMPLETADO: {ok} figuritas descargadas!")
        else:
            print(f"COMPLETADO: {ok} OK, {fail} fallaron")
            print("Fallaron:", ", ".join(failed_list[:20]))

asyncio.run(main())

print(f"\n{'='*40}")
print(f"COMPLETADO: {ok} descargadas, {fail} fallaron")
if failed_list:
    print(f"Fallaron: {', '.join(failed_list)}")
print(f"Guardadas en: {os.path.abspath(OUTPUT_DIR)}")
