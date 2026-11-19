"""Параметры системы (значения из технических требований ЛР № 1)."""

from dataclasses import dataclass

METRICS = ("cpu", "ram")


@dataclass(frozen=True)
class Settings:
    period_s: float = 1.0       # период опроса источника (частота выборки 1 Гц)
    buffer_size: int = 600      # ёмкость кольцевого буфера: 600 отсчётов = 10 минут
    window: int = 5             # окно скользящего среднего, отсчётов
    store_every: int = 5        # запись сглаженного значения каждые 5 тактов (5 с)
    min_value: float = 0.0      # допустимый диапазон отсчёта, %
    max_value: float = 100.0
