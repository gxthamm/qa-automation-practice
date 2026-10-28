from playwright.sync_api import Page, expect


def test_order_button_by_test_id(page: Page):
    """Кнопка заказа найдена по тестовому идентификатору."""
    page.goto("/?promo=random")
    page.get_by_test_id("order-btn").click()
    expect(page.get_by_test_id("result")).to_be_visible()
