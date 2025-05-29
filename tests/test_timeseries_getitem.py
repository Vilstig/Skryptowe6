import pytest
from datetime import datetime, date, timedelta
from typing import Union
from src.time_series import TimeSeries


# Pomocnicza funkcja do tworzenia obiektu TimeSeries
def create_timeseries(values) -> TimeSeries:
    base_date = datetime(2025, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(len(values))]
    return TimeSeries(
        indicator_name="PM10",
        station_code="ST01",
        averaging_time="1h",
        dates=dates,
        values=values,
        unit="µg/m³"
    )

# i. test indeksu całkowitego
def test_getitem_by_index():
    ts = create_timeseries([1.0, 2.0, 3.0])
    dt, val = ts[1]
    assert isinstance(dt, datetime)
    assert val == 2.0

# ii. test slice
def test_getitem_by_slice():
    ts = create_timeseries([1.0, 2.0, 3.0])
    sliced = ts[0:2]
    assert len(sliced) == 2
    assert sliced[0][1] == 1.0
    assert sliced[1][1] == 2.0

# iii. test istniejącej daty (datetime.date)
def test_getitem_by_existing_date():
    ts = create_timeseries([10.0, 20.0, 30.0])
    target_date = ts.dates[1].date()
    value = ts[target_date]
    assert value == 20.0

# iv. test nieistniejącej daty (KeyError)
def test_getitem_by_nonexistent_date():
    ts = create_timeseries([10.0, 20.0, 30.0])
    non_existing = date(2050, 1, 1)
    with pytest.raises(KeyError):
        _ = ts[non_existing]
