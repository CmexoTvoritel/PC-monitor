"""Предварительная обработка: скользящие средние."""


def moving_average(values) -> float:
    """Простое скользящее среднее (SMA) по переданному окну.

    Это частный случай цифрового КИХ-фильтра Yn = Σ X(n-j)·Bj
    с одинаковыми коэффициентами Bj = 1/N.
    """
    values = list(values)
    if not values:
        raise ValueError("Пустое окно")
    return sum(values) / len(values)


class ExponentialMovingAverage:
    """Экспоненциальное скользящее среднее: EMA = P·α + EMAprev·(1 − α), α = 2/(N + 1).

    Используется для сравнения с основным методом (SMA) в отчёте.
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("N должно быть не меньше 1")
        self.alpha = 2 / (n + 1)
        self.value = None

    def update(self, p: float) -> float:
        self.value = p if self.value is None else p * self.alpha + self.value * (1 - self.alpha)
        return self.value
