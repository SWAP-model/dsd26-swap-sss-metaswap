"""Live preview of the deck, without quarto preview's overlapping renders.

    pixi run preview [DECK.qmd] [PORT]          (python tools/live.py DECK.qmd PORT inside the pixi environment)

Watches the deck, the theme (*.scss), partials/, logos/ and figures/; on a change it runs one `quarto render` at a
time (a change during a render queues exactly one more), then tells open pages to reload. Serves _site on
127.0.0.1:PORT (forward the port over ssh to watch from another machine). quarto preview was set aside: two renders
overlapping deleted the reveal.js libraries, and it did not watch the theme.
"""
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
deck, port = sys.argv[1], int(sys.argv[2])
site = root / "_site"
version = 0
cond = threading.Condition()

RELOAD = (b"<script>(function(){var v=null;var es=new EventSource('/__reload');"
          b"es.onmessage=function(e){if(v!==null&&e.data!==v){location.reload();}v=e.data;};})();</script>")


def watched():
    files = [root / deck, *root.glob("*.scss"), *(root / "partials").glob("*"), *(root / "logos").glob("*"),
             *(root / "figures").glob("*")]
    return {f: f.stat().st_mtime for f in files if f.exists()}


def render():
    global version
    t0 = time.time()
    r = subprocess.run(["quarto", "render", deck], cwd=root, capture_output=True, text=True)
    out = r.stdout + r.stderr
    problems = [line for line in out.splitlines() if "ERROR" in line or "WARN" in line]
    print(f"[{time.strftime('%H:%M:%S')}] render exit {r.returncode} in {time.time() - t0:.0f} s", flush=True)
    for line in problems:
        print("   ", line, flush=True)
    if r.returncode == 0:
        with cond:
            version += 1
            cond.notify_all()


def watch():
    seen = watched()
    render()
    while True:
        time.sleep(1)
        if watched() != seen:
            time.sleep(1.5)  # let an editor finish writing
            seen = watched()
            render()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(site), **k)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/__reload":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            try:
                last = None
                while True:
                    with cond:
                        if last == version:
                            cond.wait(timeout=15)
                        v = version
                    self.wfile.write(f"data: {v}\n\n".encode())
                    self.wfile.flush()
                    last = v
            except (BrokenPipeError, ConnectionResetError):
                return
        path = self.path.split("#")[0].split("?")[0]
        if path.endswith(".html"):
            f = site / path.lstrip("/")
            if f.is_file():
                # the last </body>: embedded plugins (speaker notes) carry "</body>" in strings
                html = f.read_bytes()
                i = html.rfind(b"</body>")
                body = html[:i] + RELOAD + html[i:] if i >= 0 else html
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
                return
        super().do_GET()


threading.Thread(target=watch, daemon=True).start()
print(f"serving http://127.0.0.1:{port}/{deck.replace('.qmd', '.html')}", flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
