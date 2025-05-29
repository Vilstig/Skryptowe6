from datetime import datetime

from src.time_series import TimeSeries


def create_timeseries(values):
    return TimeSeries(indicator_name='PM10',
                      station_code='123',
                      averaging_time='1g',
                      dates=[
                          datetime(2024, 5, 1, 12, 0),
                          datetime(2024, 5, 1, 13, 0),
                          datetime(2024, 5, 1, 14, 0),
                      ],
                      values=values,
                      unit='m'
                      )

def test_timeseries_mean_std_full():
    ts = create_timeseries([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])

    assert ts.mean == 5
    assert ts.std == 2

def test_timeseries_mean_std_spotty():
    ts = create_timeseries([2.0, 4.0, 4.0, None, 4.0, 5.0, 5.0, 7.0, None, 9.0])

    assert ts.mean == 5
    assert ts.std == 2