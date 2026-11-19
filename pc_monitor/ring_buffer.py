"""Кольцевой буфер фиксированной ёмкости."""


class RingBuffer:
    """Хранит последние `capacity` значений.

    Память выделяется один раз. Указатель записи движется по кругу:
    когда буфер заполнен, новое значение записывается на место самого старого.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Ёмкость буфера должна быть положительной")
        self._data = [None] * capacity
        self._capacity = capacity
        self._head = 0        # индекс, куда будет записано следующее значение
        self._size = 0

    def append(self, value) -> None:
        self._data[self._head] = value
        self._head = (self._head + 1) % self._capacity
        self._size = min(self._size + 1, self._capacity)

    def last(self, n: int) -> list:
        """Последние n значений в порядке поступления (если их меньше — сколько есть)."""
        n = min(n, self._size)
        start = (self._head - n) % self._capacity
        return [self._data[(start + i) % self._capacity] for i in range(n)]

    def items(self) -> list:
        """Всё содержимое буфера от самого старого значения к самому новому."""
        return self.last(self._size)

    @property
    def capacity(self) -> int:
        return self._capacity

    def __len__(self) -> int:
        return self._size
