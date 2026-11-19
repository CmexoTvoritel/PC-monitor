"""Временное сохранение результатов в CSV (до появления базы данных в ЛР № 4)."""

import csv
from pathlib import Path


class CsvWriter:
    def __init__(self, folder: Path):
        folder.mkdir(parents=True, exist_ok=True)
        self._raw_f = open(folder / "samples.csv", "w", newline="", encoding="utf-8")
        self._agg_f = open(folder / "aggregated.csv", "w", newline="", encoding="utf-8")
        self.raw = csv.writer(self._raw_f)
        self.agg = csv.writer(self._agg_f)
        self.raw.writerow(["ts_utc", "metric", "raw", "valid", "sma"])
        self.agg.writerow(["ts_utc", "metric", "value"])

    def write(self, results):
        for r in results:
            sma = "" if r.smoothed is None else f"{r.smoothed:.2f}"
            ts = r.ts_utc.isoformat(timespec="milliseconds")
            self.raw.writerow([ts, r.metric, r.raw, int(r.valid), sma])
            if r.stored:
                self.agg.writerow([ts, r.metric, f"{r.smoothed:.2f}"])

    def close(self):
        self._raw_f.close()
        self._agg_f.close()
