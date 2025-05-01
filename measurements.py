import os
import re

from data_parser import parse_measures
from time_series import TimeSeries


class Measurements:
    def __init__(self, directory):
        self.directory = directory
        self.files = {}  # (param, freq, year) -> filepath
        self.loaded_series = {}  # (param, freq, year, station_code) -> TimeSeries

        # Wzorzec: np. "benzen_1g_2020.csv"
        pattern = re.compile(r"(?P<year>\d{4})_(?P<param>\w+)_(?P<freq>\w+)\.csv")

        for filename in os.listdir(directory):
            match = pattern.fullmatch(filename)
            if match:
                key = (int(match["year"]), match["param"], match["freq"])
                self.files[key] = os.path.join(directory, filename)

    def __len__(self):
        # Liczba możliwych do załadowania TimeSeries = suma liczby stacji w plikach
        count = 0
        for key in self.files:
            df, unit = parse_measures(self.files[key])
            count += len(df.columns) - 1  # zakładamy, że pierwsza kolumna to czas
        return count

    def __contains__(self, parameter_name):
        return any(key[1] == parameter_name for key in self.files)

    def _load_series_from_file(self, year, param, freq):
        key = (year, param, freq)
        if key not in self.files:
            raise FileNotFoundError(f"No file for: {key}")
        df, unit = parse_measures(self.files[key])
        for i in range(1, df.columns.size):
            ts = TimeSeries.load_ts_from_dataframe(df, i, unit)
            self.loaded_series[(year, param, freq, ts.station_code)] = ts

    def _ensure_loaded(self, year, param, freq):
        if not any((y, p, f) == (year, param, freq) for (y, p, f, _) in self.loaded_series):
            self._load_series_from_file(year, param, freq)

    def get_by_parameter(self, param_name):
        results = []
        for (year, param, freq) in self.files:
            if param == param_name:
                self._ensure_loaded(year, param, freq)
                for (y, p, f, station) in self.loaded_series:
                    if (y, p, f) == (year, param, freq):
                        results.append(self.loaded_series[(y, p, f, station)])
        return results

    def get_by_station(self, station_code):
        results = []
        for (year, param, freq) in self.files:
            print(year, param, freq)
            self._ensure_loaded(year, param, freq)
        for key, series in self.loaded_series.items():
            if key[3] == station_code:
                results.append(series)
        return results