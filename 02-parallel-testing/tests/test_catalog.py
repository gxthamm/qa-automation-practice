import time

import pytest


@pytest.mark.parametrize("item_id", range(10))
def test_catalog_item(item_id):
    time.sleep(0.5)  # имитация запроса к каталогу
    assert item_id >= 0
