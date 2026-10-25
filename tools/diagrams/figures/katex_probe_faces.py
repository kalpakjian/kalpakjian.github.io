"""Measure, in a real browser, which KaTeX font faces the page's math uses.

Static CSS reasoning is fragile: KaTeX binds families to classes through
several overlapping rules. Letting Chrome tell us which face actually
rendered each glyph is exact.

Emits the set of KaTeX_<Family>-<Variant> file stems to embed.
"""
import json
import os
import re
import subprocess
import sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9402
PAGE = sys.argv[1]
OUTJSON = sys.argv[2]

# minimal CDP client
def ws_connect(url):
    import base64, socket, struct, time
    m = re.match(r"ws://([^:/]+):(\d+)(/.*)", url)
    host, port, path_ = m.group(1), int(m.group(2)), m.group(3)
    s = socket.create_connection((host, port), timeout=30)
    key = base64.b64encode(os.urandom(16)).decode()
    s.sendall(("GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\n"
               "Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
               "Sec-WebSocket-Version: 13\r\n\r\n" % (path_, host, port, key)).encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)

    def send(obj):
        data = json.dumps(obj).encode("utf-8")
        hdr = bytearray([0x81])
        n = len(data)
        if n < 126:
            hdr.append(0x80 | n)
        elif n < 65536:
            hdr.append(0x80 | 126)
            hdr += struct.pack(">H", n)
        else:
            hdr.append(0x80 | 127)
            hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        s.sendall(bytes(hdr) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv():
        h = s.recv(2)
        ln = h[1] & 0x7F
        if ln == 126:
            ln = struct.unpack(">H", s.recv(2))[0]
        elif ln == 127:
            ln = struct.unpack(">Q", s.recv(8))[0]
        buf = b""
        while len(buf) < ln:
            buf += s.recv(ln - len(buf))
        return buf.decode("utf-8", "ignore")

    def call(method, params=None, want_id=None):
        send({"id": want_id, "method": method, "params": params or {}})
        deadline = time.time() + 45
        while time.time() < deadline:
            s.settimeout(25)
            try:
                msg = recv()
            except socket.timeout:
                break
            try:
                d = json.loads(msg)
            except Exception:
                continue
            if d.get("id") == want_id:
                return d
        return None

    return call


proc = subprocess.Popen(
    [CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=%d" % PORT,
     "--window-size=1280,900", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)

JS = r"""
(function(){
  var out = {};
  var els = document.querySelectorAll('.katex-html *');
  for (var i=0;i<els.length;i++){
    var e = els[i];
    if (!e.textContent || !e.textContent.trim()) continue;
    var cs = getComputedStyle(e);
    var fam = cs.fontFamily || '';
    var w = cs.fontWeight || '';
    var st = cs.fontStyle || '';
    var m = fam.match(/KaTeX_[A-Za-z]+/);
    if (!m) continue;
    var key = m[0];
    if (!out[key]) out[key] = {};
    out[key][w + '/' + st] = (out[key][w + '/' + st] || 0) + 1;
  }
  return JSON.stringify(out);
})()
"""

try:
    for _ in range(60):
        try:
            import urllib.request
            with urllib.request.urlopen("http://127.0.0.1:%d/json/list" % PORT, timeout=2):
                break
        except Exception:
            time.sleep(0.5)

    import urllib.request
    req = urllib.request.Request("http://127.0.0.1:%d/json/new?%s" % (PORT, PAGE), method="PUT")
    with urllib.request.urlopen(req, timeout=10) as r:
        target = json.loads(r.read().decode())
    call = ws_connect(target["webSocketDebuggerUrl"])
    call("Page.enable", want_id=1)
    call("Page.navigate", {"url": PAGE}, want_id=2)
    import time
    time.sleep(10)

    res = call("Runtime.evaluate", {"expression": JS, "returnByValue": True}, want_id=3)
    val = res.get("result", {}).get("result", {}).get("value") if res else None
    if not val:
        print("NO RESULT")
        sys.exit(1)
    data = json.loads(val)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    io_open = open(OUTJSON, "w", encoding="utf-8")
    io_open.write(json.dumps(data, ensure_ascii=False))
    io_open.close()
finally:
    try:
        proc.terminate()
    except Exception:
        pass
