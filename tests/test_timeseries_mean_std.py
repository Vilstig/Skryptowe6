from tests.test_utils import create_timeseries

def test_timeseries_mean_std_full():
    ts = create_timeseries([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])

    assert ts.mean == 5
    assert ts.std == 2

def test_timeseries_mean_std_spotty():
    ts = create_timeseries([2.0, 4.0, 4.0, None, 4.0, 5.0, 5.0, 7.0, None, 9.0])

    assert ts.mean == 5
    assert ts.std == 2