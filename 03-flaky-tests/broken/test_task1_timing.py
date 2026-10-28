from playwright.sync_api import Page


def test_order_is_placed(page: Page):
    """Заказ оформляется (с паузой) — исходный нестабильный вариант."""
    page.goto("/")
    page.get_by_test_id("order-btn").click()
    page.wait_for_timeout(1500)  # пауза «с запасом»
    visible = page.get_by_test_id("result").is_visible()
    assert visible is True
