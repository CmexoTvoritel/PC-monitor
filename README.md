# ПК-Монитор

Учебная информационная система наблюдения за нагрузкой компьютера.
Раз в секунду считывает загрузку процессора (CPU) и занятость оперативной памяти (RAM),
проверяет и сглаживает отсчёты, раз в 5 секунд формирует значение для сохранения.

Состояние: **ЛР № 2** — реализованы приём данных, кольцевой буфер, синхронизация выборки
и предварительная обработка. База данных, защита и веб-интерфейс появятся в ЛР № 4.

## Состав

| Модуль | Назначение |
| --- | --- |
| `pc_monitor/source.py` | Блок приёма: счётчики ОС через библиотеку psutil |
| `pc_monitor/sampler.py` | Синхронизация выборки: такт 1 с без накопления дрейфа |
| `pc_monitor/validation.py` | Проверка отсчёта: конечное число 0–100 % |
| `pc_monitor/ring_buffer.py` | Кольцевой буфер на 600 отсчётов (10 минут) |
| `pc_monitor/filters.py` | Скользящее среднее SMA (основное) и EMA (для сравнения) |
| `pc_monitor/processing.py` | Обработчик: проверка → буфер → SMA → запись раз в 5 с |
| `pc_monitor/output.py` | Временная запись результатов в CSV |
| `pc_monitor/config.py` | Параметры системы |

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows;  source .venv/bin/activate — Linux/macOS
pip install -r requirements-dev.txt

python -m pc_monitor --duration 120   # сбор 2 минуты; без --duration — до Ctrl+C
python tools/load_test.py             # (в другом окне) тестовая нагрузка на CPU по расписанию
python tools/plot_signal.py           # график data/samples.csv → docs/signal.png
python -m pytest                      # автоматические тесты
```

Результаты: `data/samples.csv` — все отсчёты со сглаженными значениями,
`data/aggregated.csv` — значения, сформированные раз в 5 с.
