from tests.test_utils import create_timeseries
from src.series_validator import ZeroSpikeDetector

def test_zero_spike_detected():
    time_series = create_timeseries([5.0, 0.0, None, 0.0, 1.0])
    detector = ZeroSpikeDetector(3)
    assert any(['2024-05-01 13:00:00' in detection for detection in detector.analyze(time_series)])

def test_zero_spike_none():
    time_series = create_timeseries([5.0, 0.0, None, 1.0, None])
    detector = ZeroSpikeDetector(3)
    assert detector.analyze(time_series) == []