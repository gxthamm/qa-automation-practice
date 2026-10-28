from api import register_endpoint
from users import InMemoryUserRepository, UserService


class FakeMailer:
    def __init__(self):
        self.sent = []

    def send(self, to, text):
        self.sent.append((to, text))


def build_service():
    return UserService(InMemoryUserRepository(), FakeMailer())


def test_register_endpoint_returns_201_and_email():
    """Smoke-тест верхнего слоя: запрос → код 201 и тело ответа."""
    status, body = register_endpoint(
        build_service(), {"email": "anna@example.com", "password": "secret123"}
    )
    assert status == 201
    assert body == {"email": "anna@example.com"}
