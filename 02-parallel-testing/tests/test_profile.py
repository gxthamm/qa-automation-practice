import json
import time

import pytest


def save_profile(path, name):
    path.write_text(json.dumps({"name": name}), encoding="utf-8")


def load_profile(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name", ["Анна", "Борис", "Вера", "Глеб", "Дина", "Егор", "Жанна", "Захар"]
)
def test_profile_name(name, tmp_path):
    # у каждого теста свой файл: изоляция общего состояния
    profile = tmp_path / "profile.json"
    save_profile(profile, name)
    time.sleep(0.3)  # имитация работы приложения
    assert load_profile(profile)["name"] == name
