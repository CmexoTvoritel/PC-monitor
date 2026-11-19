"""Обработчик: проверка → буфер → сглаживание → агрегация раз в 5 с."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .config import METRICS, Settings
from .filters import moving_average
from .ring_buffer import RingBuffer
from .validation import is_valid


@dataclass(frozen=True)
class Processed:
    """Результат одного такта для одной метрики."""
    ts_utc: datetime
    metric: str
    raw: object                 # значение от источника как есть
    valid: bool
    smoothed: Optional[float]   # SMA по последним `window` допустимым отсчётам
    stored: bool                # True — значение подлежит записи (раз в store_every тактов)


class Processor:
    def __init__(self, settings: Settings = Settings()):
        self.s = settings
        self.buffers = {m: RingBuffer(settings.buffer_size) for m in METRICS}
        self.rejected = {m: 0 for m in METRICS}
        self._tick = 0

    def process(self, sample) -> list:
        self._tick += 1
        store_now = self._tick % self.s.store_every == 0
        results = []
        for m in METRICS:
            raw = sample.values.get(m)
            ok = is_valid(raw, self.s.min_value, self.s.max_value)
            buf = self.buffers[m]
            if ok:
                buf.append(raw)
            else:
                self.rejected[m] += 1          # недопустимый отсчёт пропускается
            smoothed = moving_average(buf.last(self.s.window)) if len(buf) else None
            results.append(Processed(sample.ts_utc, m, raw, ok, smoothed,
                                     store_now and smoothed is not None))
        return results
