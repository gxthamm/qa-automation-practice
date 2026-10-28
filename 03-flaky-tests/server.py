import json
import random
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 3000
ROOT = Path(__file__).parent

orders_by_user = {}  # {имя_пользователя: [заказы]}
next_id = 1
lock = Lock()


class Handler(BaseHTTPRequestHandler):
    def _user(self):
        query = parse_qs(urlparse(self.path).query)
        return query.get("user", ["guest"])[0]

    def _send(self, status, body=b"", content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, data):
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/orders":
            with lock:
                orders = list(orders_by_user.get(self._user(), []))
            self._json(200, orders)
        elif path in ("/", "/index.html"):
            html = (ROOT / "public" / "index.html").read_bytes()
            self._send(200, html, "text/html")
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        global next_id
        if urlparse(self.path).path != "/api/orders":
            return self._json(404, {"error": "not found"})
        # Обработка заказа занимает от 0,3 до 2 секунд
        time.sleep(random.uniform(0.3, 2.0))
        with lock:
            order = {"id": next_id, "item": "Книга «Тестирование ПО»"}
            next_id += 1
            orders_by_user.setdefault(self._user(), []).append(order)
        self._json(201, order)

    def do_DELETE(self):
        if urlparse(self.path).path != "/api/orders":
            return self._json(404, {"error": "not found"})
        with lock:
            orders_by_user[self._user()] = []
        self._send(204)

    def log_message(self, format, *args):
        pass  # не засоряем вывод тестов служебными сообщениями


if __name__ == "__main__":
    print(f"Магазин запущен: http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
