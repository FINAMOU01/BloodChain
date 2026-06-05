"""Blockchain Gateway - HTTP server for blockchain interactions."""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from blockchain_service import register_bag


class GatewayHandler(BaseHTTPRequestHandler):
    def _respond(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health/":
            return self._respond(200, {"status": "ok"})
        self._respond(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/register-bag/":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            result = register_bag(body.get("bag_id", ""), body.get("blood_type", ""))
            return self._respond(200, result)
        self._respond(404, {"error": "not found"})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


def main():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), GatewayHandler)
    print(f"Blockchain gateway service running on port {port}...")
    server.serve_forever()


if __name__ == "__main__":
    main()
