import pytest
from playwright.sync_api import Page


@pytest.mark.quarantine
def test_order_is_placed(page: Page):
    """Копия нестабильного теста из задания 1 — в карантине."""
    page.goto("/")
    page.get_by_test_id("order-btn").click()
    page.wait_for_timeout(1500)
    visible = page.get_by_test_id("result").is_visible()
    assert visible is True
