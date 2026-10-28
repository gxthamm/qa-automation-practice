"""Замеры для отчёта по параллельному тестированию.

Запускает pytest в разных режимах, собирает время и число тестов,
складывает результаты в measurements.json.
"""

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
# задания 1-4 считаем на основном наборе из 24 тестов,
# test_profile.py из задания 5 замеряем отдельно
MAIN = ["--ignore=tests/test_profile.py", "--ignore=broken"]


def run(args):
    started = time.perf_counter()
    result = subprocess.run(
        [PY, "-m", "pytest", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=ENV,
    )
    elapsed = round(time.perf_counter() - started, 2)
    out = result.stdout + result.stderr
    match = re.search(r"in ([\d.]+)s", out)
    reported = float(match.group(1)) if match else None
    passed = re.search(r"(\d+) passed", out)
    failed = re.search(r"(\d+) failed", out)
    return {
        "args": " ".join(args),
        "wall_seconds": elapsed,
        "reported_seconds": reported,
        "passed": int(passed.group(1)) if passed else 0,
        "failed": int(failed.group(1)) if failed else 0,
        "output": out,
    }


def brief(record):
    return (
        f"{record['args']:<70} passed={record['passed']:>2} "
        f"failed={record['failed']:>2} time={record['reported_seconds']}s"
    )


def main():
    data = {"collect": run(["--collect-only", "-q", *MAIN]), "runs": []}
    print("collect:", brief(data["collect"]))

    plan = [
        ["-v", "--durations=5", *MAIN],
        ["-n", "2", *MAIN],
        ["-n", "4", *MAIN],
        ["-n", "auto", *MAIN],
        ["-n", "4", "-v", *MAIN],
    ]
    for args in plan:
        record = run(args)
        data["runs"].append(record)
        print(brief(record))

    # воркеры для четырёх медленных тестов
    verbose = next(r for r in data["runs"] if r["args"].startswith("-n 4 -v"))
    mapping = [
        line.strip()
        for line in verbose["output"].splitlines()
        if "test_build_report" in line
    ]
    data["report_workers"] = mapping

    print("\n-- статическое разбиение --")
    static = []
    for group in range(1, 5):
        record = run(["--splits", "4", "--group", str(group), *MAIN])
        static.append(record)
        print(brief(record))
    data["static"] = static

    print("\n-- запись длительностей --")
    store = run(["--store-durations", *MAIN])
    print(brief(store))
    data["store"] = store

    print("\n-- разбиение по длительности --")
    dynamic = []
    for group in range(1, 5):
        record = run(
            [
                "--splits",
                "4",
                "--group",
                str(group),
                "--splitting-algorithm",
                "least_duration",
                *MAIN,
            ]
        )
        dynamic.append(record)
        print(brief(record))
    data["dynamic"] = dynamic

    print("\n-- задание 5: общий файл (сломанный вариант, -n 4) --")
    broken = [
        run(["broken/test_profile.py", "-n", "4", "-p", "no:cacheprovider"])
        for _ in range(3)
    ]
    for record in broken:
        print(brief(record))
    data["profile_broken"] = broken

    print("\n-- задание 5: изолированный вариант (-n 4) --")
    fixed = [run(["tests/test_profile.py", "-n", "4"]) for _ in range(3)]
    for record in fixed:
        print(brief(record))
    data["profile_fixed"] = fixed

    (ROOT / "measurements.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nСохранено: measurements.json")


if __name__ == "__main__":
    main()
