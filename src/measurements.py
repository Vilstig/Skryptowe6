import os
import re

from data_parser import parse_measures
from time_series import TimeSeries
from typing import List, Dict, Tuple, Union
from series_validator import SeriesValidator


class Measurements:
    def __init__(self, directory: os.PathLike) -> None:
        self.directory = directory
        self.files: Dict[Tuple[int, str, str], str] = {}  # (year, param, freq) -> filepath
        self.loaded_series: Dict[Tuple[int, str, str, str], TimeSeries] = {}  # (year, param, freq, station_code) -> TimeSeries

        pattern: re.Pattern = re.compile(r"(?P<year>\d{4})_(?P<param>.+)_(?P<freq>\w+)\.csv")

        for filename in os.listdir(directory):
            match: Union[re.Match, None] = pattern.fullmatch(filename)
            if match:
                key: Tuple[int, str, str] = (int(match["year"]), match["param"], match["freq"])
                self.files[key] = os.path.join(directory, filename)

    def __len__(self) -> int:
        count: int = 0
        for key in self.files:
            df, unit = parse_measures(self.files[key])
            count += len(df.columns) - 1  # first column contains timestamp
        return count

    def __contains__(self, parameter_name) -> bool:
        return any(key[1] == parameter_name for key in self.files)

    def _load_series_from_file(self, year: int, param: str, freq: str) -> None:
        key: Tuple[int, str, str] = (year, param, freq)
        if key not in self.files:
            raise FileNotFoundError(f"No file for: {key}")
        df, unit = parse_measures(self.files[key])
        for i in range(1, df.columns.size):
            ts: TimeSeries = TimeSeries.load_ts_from_dataframe(df, i, unit)
            self.loaded_series[(year, param, freq, ts.station_code)] = ts

    def _ensure_loaded(self, year: int, param: str, freq: str) -> None:
        if not any((y, p, f) == (year, param, freq) for (y, p, f, _) in self.loaded_series):
            self._load_series_from_file(year, param, freq)

    def get_by_parameter(self, param_name) -> List[TimeSeries]:
        results: List[TimeSeries] = []
        for (year, param, freq) in self.files:
            if param == param_name:
                self._ensure_loaded(year, param, freq)

        for (y, p, f, station) in self.loaded_series:  # couldnt this be done better in 2 seperate loops? Yes :)
            if param_name == p:
                results.append(self.loaded_series[(y, p, f, station)])
        return results

    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        results: List[TimeSeries] = []
        for (year, param, freq) in self.files:
            # print(year, param, freq)
            self._ensure_loaded(year, param, freq)
        for key, series in self.loaded_series.items():
            if key[3] == station_code:
                results.append(series)
        return results

    def detect_all_anomalies(self, validators: List[SeriesValidator], preload: bool = False) -> Dict[Tuple[int, str, str, str], List[str]]:
        all_anomalies: Dict[Tuple[int, str, str, str], List[str]] = {}
        if preload:
            for (year, param, freq) in self.files:
                self._ensure_loaded(year, param, freq)

        for key, series in self.loaded_series.items():
            results: List[str] = []

            for validator in validators:
                results.extend(validator.analyze(series))

            if results:
                all_anomalies[key] = results

        return all_anomalies