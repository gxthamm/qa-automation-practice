"""Исходный нестабильный вариант из задания 5 (общий файл на все тесты).

Хранится отдельно от tests/, чтобы не попадать в основной прогон.
"""

import json
import time
from pathlib import Path

import pytest

PROFILE = Path("profile.json")


def save_profile(path, name):
    path.write_text(json.dumps({"name": name}), encoding="utf-8")


def load_profile(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name", ["Анна", "Борис", "Вера", "Глеб", "Дина", "Егор", "Жанна", "Захар"]
)
def test_profile_name(name):
    save_profile(PROFILE, name)
    time.sleep(0.3)  # имитация работы приложения
    assert load_profile(PROFILE)["name"] == name
