"""Блок синхронизации выборки: формирует такты строго с заданным периодом."""

import time


class Sampler:
    """Генератор тактов с компенсацией дрейфа.

    Момент k-го такта вычисляется от момента старта: t_k = t0 + k·T,
    а не «предыдущий такт + T». Поэтому задержки обработки не накапливаются.
    Если обработка задержалась больше чем на период, пропущенные такты
    не догоняются пачкой, а отбрасываются и учитываются в счётчике `missed`.
    """

    def __init__(self, period_s: float, clock=time.monotonic, sleep=time.sleep):
        if period_s <= 0:
            raise ValueError("Период должен быть положительным")
        self.period = period_s
        self._clock = clock
        self._sleep = sleep
        self.missed = 0

    def ticks(self, count=None):
        """Выдаёт номера тактов 0, 1, 2, … ; count=None — бесконечно."""
        start = self._clock()
        k = 0
        while count is None or k < count:
            target = start + k * self.period
            delay = target - self._clock()
            if delay > 0:
                self._sleep(delay)
            elif -delay >= self.period:              # опоздали на целый период и больше
                skip = int(-delay // self.period)
                self.missed += skip
                k += skip
                if count is not None and k >= count:
                    break
            yield k
            k += 1
