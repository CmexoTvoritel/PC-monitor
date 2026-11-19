"""Запуск: python -m pc_monitor [--duration СЕКУНДЫ] [--out ПАПКА]"""

import argparse
import time
from pathlib import Path

from .config import Settings
from .output import CsvWriter
from .processing import Processor
from .sampler import Sampler
from .source import PsutilSource


def _fmt(v):
    return "  —" if v is None else f"{v:5.1f}"


def run(duration=None, out=Path("data")):
    settings = Settings()
    source, processor = PsutilSource(), Processor(settings)
    sampler, writer = Sampler(settings.period_s), CsvWriter(out)
    count = None if duration is None else int(duration / settings.period_s)
    print("ПК-Монитор: сбор данных (Ctrl+C — остановка)")
    print(f"{'время UTC':<13}{'CPU':>7}{'CPU SMA':>9}{'RAM':>7}{'RAM SMA':>9}")
    t0 = time.monotonic()
    try:
        for _ in sampler.ticks(count):
            res = processor.process(source.read())
            writer.write(res)
            c, r = res
            mark = "  <- запись" if c.stored else ""
            flag = "" if c.valid and r.valid else "  ! отсчёт отброшен"
            print(f"{c.ts_utc:%H:%M:%S.%f}"[:12]
                  + f" {_fmt(c.raw):>6} {_fmt(c.smoothed):>8} {_fmt(r.raw):>6} {_fmt(r.smoothed):>8}"
                  + mark + flag)
    except KeyboardInterrupt:
        pass
    finally:
        writer.close()
    print(f"Готово: {time.monotonic() - t0:.1f} с, пропущено тактов: {sampler.missed}, "
          f"отброшено отсчётов: {processor.rejected}, "
          f"в буфере: {len(processor.buffers['cpu'])} из {settings.buffer_size}")


def main():
    p = argparse.ArgumentParser(description="ПК-Монитор: приём и сглаживание нагрузки CPU/RAM")
    p.add_argument("--duration", type=float, default=None, help="длительность, с (по умолчанию — до Ctrl+C)")
    p.add_argument("--out", type=Path, default=Path("data"), help="папка для CSV-файлов")
    a = p.parse_args()
    run(a.duration, a.out)


if __name__ == "__main__":
    main()
