# Практические работы по автоматизации тестирования

![CI](https://github.com/gxthamm/qa-automation-practice/actions/workflows/ci.yml/badge.svg)

Учебные проекты по дисциплине «Автоматизация тестирования» (Python).
Каждая папка — отдельная работа: в 1–6 лежат код, тесты и результаты прогонов, в 7–10 — PDF-отчёты.

| № | Папка | Тема | Что внутри |
|---|-------|------|------------|
| 1 | `01-behave-automation/` | Организация автоматизации тестирования с нуля | UI-тесты на behave + Playwright, `db_check.py`, Allure |
| 2 | `02-parallel-testing/` | Параллельное тестирование | pytest-xdist, pytest-split, `measure.py`, `.test_durations` |
| 3 | `03-flaky-tests/` | Нестабильные (flaky) тесты | Playwright, разбор причин, карантин, `run_experiments.py` |
| 4 | `04-mutmut/` | Мутационное тестирование | mutmut 2.5.1, MSI до/после, бонус `is_honors` |
| 5 | `05-ai-expertise/` | Экспертиза AI-текстов | стандарт SQL-скриптов и миграций, `Приложение 1` |
| 6 | `06-subcutaneous-tests/` | Подкожные тесты | unit + subcutaneous + мок внешнего API (`responses`) |
| 7 | `07-automation-tools/` | Виды и инструменты автоматизации | PDF-отчёт: HTTP-статусы и проверки API |
| 8 | `08-ci-cd-pipeline/` | CI/CD-пайплайн | PDF-отчёт: workflow, матрица, кэш, JUnit, Docker, защита ветки |
| 9 | `09-visual-regression/` | Визуальное регрессионное тестирование | PDF-отчёт: правки страницы, `maxDiffPixelRatio`, скриншоты |
| 10 | `10-certificate-analysis/` | Анализ сертификатов соответствия | PDF-отчёт: разбор сертификатов ФСТЭК/ЕАЭС |

## Запуск

Все работы используют одно виртуальное окружение в корне:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
playwright install chromium
```

Дальше — из папки нужной работы:

```bash
cd 06-subcutaneous-tests && python -m pytest -q
cd 02-parallel-testing && python measure.py
cd 03-flaky-tests && python run_experiments.py
cd 04-mutmut && mutmut run && mutmut results
cd 01-behave-automation && behave -f allure_behave.formatter:AllureFormatter -o allure-results features
```

## Результаты

Числа в отчётах получены реальными прогонами на Python 3.14.4, 16 логических ядер:

- параллельный запуск: 24 теста, последовательно 31,26 с; `-n 4` — 9,22 с (S = 3,39, E = 0,85);
- flaky: исходный тест падал в 13 из 60 запусков, после замены паузы на `expect` — 0 из 60;
- мутации: 21 мутант, MSI 33,3 % до усиления тестов и 100 % после;
- подкожные тесты: 8 тестов, каждый из двух внесённых багов ловят 2 теста.

## CI

GitHub Actions (`.github/workflows/ci.yml`) на каждый push и pull request запускает:

- `behave` — UI-сценарии перевода из работы 1;
- `parallel` — матрица из 4 шардов `pytest-split` с `least_duration` (работа 2);
- `flaky` — основной набор работы 3 без карантина;
- `mutmut` — тесты и мутационный прогон работы 4;
- `subcutaneous` — тесты работы 6.

Результаты прогонов: <https://github.com/gxthamm/qa-automation-practice/actions>.

