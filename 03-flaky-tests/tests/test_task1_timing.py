from playwright.sync_api import Page, expect


def test_order_is_placed(page: Page):
    """Заказ оформляется: ждём событие, а не фиксированное время."""
    page.goto("/")
    page.get_by_test_id("order-btn").click()
    expect(page.get_by_test_id("result")).to_be_visible()
