"""Строит график «сырой сигнал / SMA / EMA» по файлу data/samples.csv.

Запуск: python tools/plot_signal.py [data/samples.csv] [docs/signal.png] [cpu,ram]
"""

import csv
import sys
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
from pc_monitor.filters import ExponentialMovingAverage  # noqa: E402


def load(path, metric):
    t, raw, sma = [], [], []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["metric"] != metric or row["valid"] != "1":
                continue
            t.append(datetime.fromisoformat(row["ts_utc"]))
            raw.append(float(row["raw"]))
            sma.append(float(row["sma"]))
    t0 = t[0]
    return [(x - t0).total_seconds() for x in t], raw, sma


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "data/samples.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "docs/signal.png"
    metrics = (sys.argv[3] if len(sys.argv) > 3 else "cpu,ram").split(",")
    titles = {"cpu": "Загрузка CPU", "ram": "Занятость RAM"}
    fig, axes = plt.subplots(len(metrics), 1, figsize=(10, 3.4 * len(metrics)), sharex=True, squeeze=False)
    axes = axes[:, 0]
    for ax, metric in zip(axes, metrics):
        title = titles[metric]
        x, raw, sma = load(src, metric)
        ema = ExponentialMovingAverage(5)
        e = [ema.update(v) for v in raw]
        ax.plot(x, raw, color="#9aa5b1", lw=1, marker=".", ms=3, label="Сырой отсчёт (1 с)")
        ax.plot(x, sma, color="#1f5fbf", lw=2, label="SMA, N = 5")
        ax.plot(x, e, color="#d9822b", lw=1.5, ls="--", label="EMA, N = 5")
        ax.set_title(title)
        ax.set_ylabel("%")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper right", fontsize=9)
    axes[-1].set_xlabel("Время от начала записи, с")
    fig.tight_layout()
    fig.savefig(dst, dpi=150)
    print("Сохранено:", dst)


if __name__ == "__main__":
    main()
