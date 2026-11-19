from datetime import datetime, timezone
from pc_monitor.config import Settings
from pc_monitor.processing import Processor
from pc_monitor.source import RawSample


def sample(cpu, ram=50.0):
    return RawSample(datetime.now(timezone.utc), {"cpu": cpu, "ram": ram})


def test_invalid_sample_is_skipped():
    p = Processor(Settings())
    p.process(sample(20.0))
    cpu = p.process(sample(150.0))[0]
    assert not cpu.valid and cpu.smoothed == 20.0
    assert p.rejected["cpu"] == 1 and len(p.buffers["cpu"]) == 1


def test_start_uses_available_samples():
    p = Processor(Settings())
    p.process(sample(10.0))
    assert p.process(sample(30.0))[0].smoothed == 20.0


def test_store_every_fifth_tick():
    p = Processor(Settings())
    flags = [p.process(sample(10.0))[0].stored for _ in range(10)]
    assert flags == [False] * 4 + [True] + [False] * 4 + [True]
