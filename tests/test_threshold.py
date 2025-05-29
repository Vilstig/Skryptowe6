from tests.test_utils import create_timeseries
from src.series_validator import ThresholdDetector

def test_threshold_exceeded():
    time_series = create_timeseries([1.0, 3.0, 999999.0, 2.0, 1.0])
    detector = ThresholdDetector(50.0)
    assert any(['999999.0' in detection for detection in detector.analyze(time_series)])

def test_threshold_not_exceeded():
    time_series = create_timeseries([1.0, 3.0, 5.0, 2.0, 1.0])
    detector = ThresholdDetector(50.0)
    assert detector.analyze(time_series) == []