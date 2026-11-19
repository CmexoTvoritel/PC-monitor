"""Проверка допустимости отсчёта."""

import math


def is_valid(value, min_value: float = 0.0, max_value: float = 100.0) -> bool:
    """Отсчёт допустим, если это конечное число в диапазоне [min_value; max_value]."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value) and min_value <= value <= max_value
