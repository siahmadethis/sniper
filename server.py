#!/usr/bin/env python3
"""Static file server with a FRED CSV proxy.

The display in index.html first tries to fetch FRED data directly from the
browser; if that is blocked (CORS, firewall), it falls back to this server's
/api/fred endpoint, which fetches the CSV server-side.

Usage:
    python3 server.py [port]    # default port 8000

No third-party dependencies.
"""

import re
import sys
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv"
SERIES_RE = re.compile(r"^[A-Z0-9]{1,32}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/fred":
            self.handle_fred(urllib.parse.parse_qs(parsed.query))
        else:
            super().do_GET()

    def handle_fred(self, params):
        series = params.get("id", [""])[0]
        start = params.get("cosd", [""])[0]
        if not SERIES_RE.match(series):
            self.send_error(400, "invalid series id")
            return

        url = FRED_CSV + "?id=" + series
        if DATE_RE.match(start):
            url += "&cosd=" + start

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "sniper/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read()
        except Exception as exc:  # noqa: BLE001 - report any upstream failure
            self.send_error(502, f"FRED fetch failed: {exc}")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "max-age=300")
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
