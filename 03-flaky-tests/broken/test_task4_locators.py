from playwright.sync_api import Page, expect


def test_order_button_by_position(page: Page):
    """Кнопка заказа найдена по позиции в разметке"""
    page.goto("/?promo=random")  # акция показывается примерно каждому второму
    page.locator('xpath=//div[@class="container"]/div[1]/button').click()
    expect(page.get_by_test_id("result")).to_be_visible()
