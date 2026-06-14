# Local edit server for sokol-ads: serves the deck over http, persists in-browser
# text edits to ads/overrides.js, and rebuilds the PPTX on demand (POST /build).
import json, os, subprocess, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

ADS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ADS)            # presentation/ — so ../assets resolves
OVR = os.path.join(ADS, 'overrides.js')

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(302)
            self.send_header('Location', '/ads/sokol-ads.html')
            self.end_headers()
            return
        super().do_GET()

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(n) if n else b''
        if self.path == '/save':
            data = json.loads(raw.decode('utf-8') or '{}')
            with open(OVR, 'w', encoding='utf-8') as f:
                f.write('window.OVERRIDES = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
            self._json(200, {'ok': True, 'count': len(data)})
        elif self.path == '/reset':
            with open(OVR, 'w', encoding='utf-8') as f:
                f.write('window.OVERRIDES = {};\n')
            self._json(200, {'ok': True})
        elif self.path == '/build':
            log, ok = [], False
            try:
                r1 = subprocess.run(
                    ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                     os.path.join(ADS, '_shoot_ads.ps1')],
                    capture_output=True, text=True, timeout=240)
                log.append(r1.stdout[-500:])
                r2 = subprocess.run(
                    [sys.executable, os.path.join(ADS, '_build_ads_pptx.py')],
                    capture_output=True, text=True, timeout=120)
                log.append(r2.stdout[-500:])
                ok = r2.returncode == 0
            except Exception as e:
                log.append(str(e))
            self._json(200, {'ok': ok, 'log': '\n'.join(log)})
        else:
            self._json(404, {'ok': False})

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f'editing server: http://127.0.0.1:{port}/ads/sokol-ads.html', flush=True)
    HTTPServer(('127.0.0.1', port), H).serve_forever()
