"""
Servidor receptor de figuritas.
El browser le envia las imagenes como base64 y este script las guarda al disco.
Uso: python servidor_receptor.py
"""
import http.server
import base64
import json
import os
import threading

OUTPUT_DIR = os.path.join("docs", "img", "stickers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PORT = 9999
saved = [0]
failed = [0]
done_event = threading.Event()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self, *args):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if self.path == "/done":
            print(f"\n{'='*40}")
            print(f"COMPLETADO: {saved[0]} guardadas, {failed[0]} fallaron")
            self.wfile.write(b'{"ok":true}')
            done_event.set()
            return

        if self.path == "/fail":
            data = json.loads(body)
            failed[0] += 1
            print(f"  FALLO: {data.get('name','?')} (status {data.get('status','?')})")
            self.wfile.write(b'{"ok":true}')
            return

        try:
            data = json.loads(body)
            name = data["name"]
            b64  = data["b64"]
            filepath = os.path.join(OUTPUT_DIR, name)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(b64))
            saved[0] += 1
            if saved[0] % 20 == 0:
                print(f"  ... {saved[0]} figuritas guardadas")
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            failed[0] += 1
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())

    def log_message(self, *args):
        pass  # suprimir logs de cada request

print(f"Servidor receptor escuchando en puerto {PORT}...")
print("Ahora pega el codigo JavaScript en la consola del browser.\n")

server = http.server.HTTPServer(("localhost", PORT), Handler)
server_thread = threading.Thread(target=server.serve_forever, daemon=True)
server_thread.start()

done_event.wait()
server.shutdown()
print("Servidor cerrado. Listo!")
