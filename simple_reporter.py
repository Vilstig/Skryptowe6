from time_series import TimeSeries
from series_validator import OutlierDetector, ZeroSpikeDetector
from datetime import datetime, timedelta

class SimpleReporter():
    def analyze(self, series):
        return [f"Info: {series.indicator_name} at {series.station_code} has mean = {series.mean:.2f}"]
