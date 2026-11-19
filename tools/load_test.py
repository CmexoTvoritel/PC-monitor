"""Создаёт тестовую нагрузку на все ядра процессора по расписанию.

Запуск (в отдельном окне одновременно с python -m pc_monitor --duration 120):
    python tools/load_test.py
Расписание: (начало, длительность) в секундах от запуска.
"""

import multiprocessing as mp
import time

SCHEDULE = [(15, 14), (45, 2), (62, 1), (78, 22)]


def busy(seconds):
    end = time.time() + seconds
    while time.time() < end:
        pass


def main():
    t0 = time.time()
    with mp.Pool(mp.cpu_count()) as pool:
        for start, dur in SCHEDULE:
            time.sleep(max(0.0, t0 + start - time.time()))
            print(f"нагрузка {dur} с")
            pool.map(busy, [dur] * mp.cpu_count())
    print("готово")


if __name__ == "__main__":
    main()
