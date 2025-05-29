from tests.test_utils import create_timeseries
from src.series_validator import ZeroSpikeDetector, ThresholdDetector, OutlierDetector
import pytest
from src.data_parser import parse_measures
from src.time_series import TimeSeries

@pytest.mark.parametrize("outlier_param,spike_param,thresh_param", [(1, 3, 30.0), (2, 2, 60.0), (3, 1, 90.0)])
def test_detect_all_anomalies(outlier_param, spike_param, thresh_param):
    detectors = [OutlierDetector(outlier_param), ZeroSpikeDetector(spike_param), ThresholdDetector(thresh_param)]
    df, unit = parse_measures('data_S5/measurements/2023_PM10_24g.csv')

    time_series = TimeSeries.load_ts_from_dataframe(df, 2, unit)
    assert all([detector.analyze(time_series) != [] for detector in detectors])