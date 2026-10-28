"""Прогоны для отчёта по flaky-тестам: реальные числа падений и время."""

import json
import os
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
PY = sys.executable
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
RESULTS = []


def run(label, args, comment="", env_extra=None):
    started = time.perf_counter()
    env = dict(ENV)
    if env_extra:
        env.update(env_extra)
    result = subprocess.run(
        [PY, "-m", "pytest", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    elapsed = round(time.perf_counter() - started, 2)
    out = result.stdout + result.stderr
    failed = re.search(r"(\d+) failed", out)
    passed = re.search(r"(\d+) passed", out)
    failed_names = [
        line.strip() for line in out.splitlines() if line.startswith("FAILED")
    ]
    record = {
        "label": label,
        "args": " ".join(args),
        "comment": comment,
        "seconds": elapsed,
        "failed": int(failed.group(1)) if failed else 0,
        "passed": int(passed.group(1)) if passed else 0,
        "failed_names": failed_names,
        "tail": [line for line in out.splitlines() if line.strip()][-3:],
    }
    RESULTS.append(record)
    print(
        f"{label:<34} passed={record['passed']:>2} failed={record['failed']:>2} "
        f"{elapsed:>6.1f}s"
    )
    return record


def main():
    # Задание 1: исходный тест с паузой 1,5 с — три серии по 20 запусков
    for series in range(1, 4):
        run(f"task1_broken_series{series}",
            ["broken/test_task1_timing.py", "--count=20", "--tb=no", "-q"])
    run("task1_broken_error", ["broken/test_task1_timing.py", "--count=20", "-x", "-q"],
        "текст ошибки первого падения")

    # Задание 2: исправленный тест — три серии по 20 запусков
    for series in range(1, 4):
        run(f"task2_fixed_series{series}",
            ["tests/test_task1_timing.py", "--count=20", "--tb=no", "-q"])
    run("task2_timeout_1000", ["tests/test_task1_timing.py", "--count=20", "--tb=no", "-q"],
        "эксперимент с таймаутом 1000 мс", env_extra={"EXPECT_TIMEOUT": "1000"})

    # Задание 3: общее состояние
    run("task3_broken_all", ["broken/test_task3_state.py", "--tb=no", "-q"])
    for key in ("counter", "one_item", "empty"):
        run(f"task3_broken_only_{key}",
            ["broken/test_task3_state.py", "-k", key, "--tb=no", "-q"])
    for series in range(1, 6):
        run(f"task3_broken_parallel{series}",
            ["broken/test_task3_state.py", "-n", "3", "--tb=no", "-q", "-rf"])
    for series in range(1, 6):
        run(f"task3_fixed_parallel{series}",
            ["tests/test_task3_state.py", "-n", "3", "--tb=no", "-q"])
    run("task3_fixed_all", ["tests/test_task3_state.py", "--tb=no", "-q"])

    # Задание 4: хрупкие локаторы
    for series in range(1, 3):
        run(f"task4_broken_series{series}",
            ["broken/test_task4_locators.py", "--count=20", "--tb=no", "-q"])
    run("task4_broken_error",
        ["broken/test_task4_locators.py", "--count=20", "-x", "-q"],
        "текст ошибки первого падения")
    run("task4_fixed_series",
        ["tests/test_task4_locators.py", "--count=20", "--tb=no", "-q"])

    # Задание 5: диагностика и карантин
    run("task5_demo_10", ["broken/test_task5_demo.py", "-m", "quarantine",
                          "--count=10", "--tb=no", "-q"])
    run("task5_main_without_quarantine", ["tests", "-m", "not quarantine", "--tb=short", "-q"])
    run("task5_quarantine_10", ["broken/test_task5_demo.py", "-m", "quarantine",
                                "--count=10", "--tb=no", "-q"])
    run("task5_fixed_20", ["tests/test_task5_demo.py", "--count=20", "--tb=no", "-q"])

    (ROOT / "experiments.json").write_text(
        json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nСохранено: experiments.json")


if __name__ == "__main__":
    main()
