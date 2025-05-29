from src.time_series import TimeSeries
from datetime import datetime

def create_timeseries(values):
    return TimeSeries(indicator_name='PM10',
                      station_code='123',
                      averaging_time='1g',
                      dates=[
                          datetime(2024, 5, 1, 12, 0),
                          datetime(2024, 5, 1, 13, 0),
                          datetime(2024, 5, 1, 14, 0),
                          datetime(2024, 5, 1, 15, 0),
                          datetime(2024, 5, 1, 16, 0),
                      ],
                      values=values,
                      unit='m'
                      )