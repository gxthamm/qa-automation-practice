import uuid

from playwright.sync_api import Page, expect


def test_counter_shows_one(page: Page):
    """После заказа счётчик показывает 1"""
    user = uuid.uuid4().hex
    page.goto(f"/?user={user}")
    page.get_by_test_id("order-btn").click()
    expect(page.get_by_test_id("result")).to_be_visible()
    expect(page.get_by_test_id("orders-count")).to_have_text("Заказов: 1")


def test_list_has_one_item(page: Page):
    """После заказа в списке одна позиция"""
    user = uuid.uuid4().hex
    page.goto(f"/?user={user}")
    page.get_by_test_id("order-btn").click()
    expect(page.get_by_test_id("result")).to_be_visible()
    expect(page.locator("#orders li")).to_have_count(1)


def test_list_is_empty_on_first_visit(page: Page):
    """При первом открытии список пуст"""
    user = uuid.uuid4().hex
    page.goto(f"/?user={user}")
    expect(page.get_by_test_id("orders-count")).to_have_text("Заказов: 0")
