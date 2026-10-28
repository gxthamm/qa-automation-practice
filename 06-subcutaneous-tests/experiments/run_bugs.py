"""Эксперимент из заданий 2.2-2.4: два бага, проверка какие тесты падают."""

import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "users.py"
BACKUP = ROOT / "users.py.bak"

BUGS = {
    "Баг 1: закомментирован self.repository.add(user)": (
        "        self.repository.add(user)",
        "        # self.repository.add(user)",
    ),
    "Баг 2: закомментирован self.mailer.send(...)": (
        '        self.mailer.send(email, "Добро пожаловать!")',
        '        # self.mailer.send(email, "Добро пожаловать!")',
    ),
}


def run_tests():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--tb=no", "-rf"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    summary = lines[-1] if lines else "(нет вывода)"
    failed = [line for line in lines if line.startswith("FAILED")]
    return summary, failed


def main():
    shutil.copy(SOURCE, BACKUP)
    try:
        for title, (old, new) in BUGS.items():
            text = BACKUP.read_text(encoding="utf-8")
            if old not in text:
                raise SystemExit(f"Не найдена строка: {old}")
            SOURCE.write_text(text.replace(old, new), encoding="utf-8")
            summary, failed = run_tests()
            print("=" * 70)
            print(title)
            print(summary)
            for line in failed:
                print(line)
    finally:
        shutil.copy(BACKUP, SOURCE)
        BACKUP.unlink(missing_ok=True)
        print("=" * 70)
        print("users.py восстановлен:", run_tests()[0])


if __name__ == "__main__":
    main()
