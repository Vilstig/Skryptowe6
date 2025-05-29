from src.series_validator import OutlierDetector
from tests.test_utils import create_timeseries

def test_outlier_detection_found():
    time_series = create_timeseries([5.0, 4.0, 5.5, 6.0, 24.0])
    detector = OutlierDetector(1)
    assert any(['2024-05-01 16:00:00' in detection for detection in detector.analyze(time_series)])

def test_outlier_detection_none():
    time_series = create_timeseries([5.0, 5.0, 5.0, 5.0, 5.0])
    detector = OutlierDetector(1)
    assert detector.analyze(time_series) == []