from pc_monitor.sampler import Sampler


class FakeClock:
    """Виртуальные часы: время идёт только при вызове sleep или advance."""
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t

    def sleep(self, d):
        self.t += d


def test_ticks_without_drift():
    clk = FakeClock()
    s = Sampler(1.0, clock=clk, sleep=clk.sleep)
    times = []
    for _ in s.ticks(5):
        times.append(clk.t)
        clk.t += 0.3                     # обработка занимает 0,3 с
    assert times == [100.0, 101.0, 102.0, 103.0, 104.0]   # дрейф не накапливается
    assert s.missed == 0


def test_missed_ticks_are_skipped():
    clk = FakeClock()
    s = Sampler(1.0, clock=clk, sleep=clk.sleep)
    got = []
    for k in s.ticks(6):
        got.append(k)
        if k == 1:
            clk.t += 2.5                 # «зависание» на 2,5 с: такт 2 (t=102) целиком пропущен
    assert s.missed == 1
    assert got == [0, 1, 3, 4, 5]    # такт 3 выполняется с опозданием 0,5 с, дальше снова по графику
