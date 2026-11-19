"""Блок приёма данных: программно опрашиваемый цифровой источник (счётчики ОС через psutil)."""

from dataclasses import dataclass
from datetime import datetime, timezone

import psutil


@dataclass(frozen=True)
class RawSample:
    """Сырой отсчёт: время в UTC и значения метрик в процентах (None — значение не получено)."""
    ts_utc: datetime
    values: dict


class PsutilSource:
    """Читает загрузку процессора и занятость оперативной памяти.

    psutil.cpu_percent(interval=None) возвращает загрузку за время, прошедшее
    с предыдущего вызова, поэтому при создании объекта выполняется
    «пустой» первый вызов, а дальше каждый такт даёт загрузку за последнюю секунду.
    """

    def __init__(self):
        psutil.cpu_percent(interval=None)

    def read(self) -> RawSample:
        ts = datetime.now(timezone.utc)
        values = {}
        try:
            values["cpu"] = float(psutil.cpu_percent(interval=None))
        except Exception:          # ошибка источника = недопустимый отсчёт
            values["cpu"] = None
        try:
            values["ram"] = float(psutil.virtual_memory().percent)
        except Exception:
            values["ram"] = None
        return RawSample(ts, values)
