import os
import threading
from http.server import ThreadingHTTPServer

import pytest
from playwright.sync_api import expect

from server import HOST, PORT, Handler

# Таймаут проверок: по умолчанию 5 секунд. Переменная окружения нужна
# только для эксперимента из задания 2 (пункт 5), где ставится 1000 мс.
expect.set_options(timeout=int(os.environ.get("EXPECT_TIMEOUT", "5000")))

_server = None


def pytest_configure(config):
    """Запускает магазин перед тестами: один раз, в основном процессе."""
    global _server
    if hasattr(config, "workerinput"):  # рабочий процесс pytest-xdist: сервер уже запущен
        return
    _server = ThreadingHTTPServer((HOST, PORT), Handler)
    threading.Thread(target=_server.serve_forever, daemon=True).start()


def pytest_unconfigure(config):
    if _server is not None:
        _server.shutdown()
        _server.server_close()


@pytest.fixture(autouse=True)
def short_action_timeout(page):
    page.set_default_timeout(5000)  # клик и другие действия ждут не дольше 5 секунд
