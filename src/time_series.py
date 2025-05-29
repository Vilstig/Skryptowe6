from datetime import datetime, date
from typing import Union, Any, Tuple, List

import numpy as np
import pandas as pd


class TimeSeries:
    def __init__(self, indicator_name: str, station_code: str, averaging_time: str, dates: list[datetime],
                 values: list[Union[float, None]], unit: str) -> None:
        self.indicator_name = indicator_name  # np. "PM10"
        self.station_code = station_code  # kod stacji
        self.averaging_time = averaging_time  # np. "1h"
        self.dates = dates  # lista obiektów datetime
        self.values = np.array([np.nan if v is None else v for v in values],
                               dtype=float)  # tablica numpy wartości (float lub None)
        self.unit = unit  # np. "µg/m³"

    def __str__(self) -> str:
        return f'Station code: {self.station_code}, Indicator name: {self.indicator_name}, Averaging time: {self.averaging_time}'

    def __repr__(self) -> str:
        return (f"TimeSeries(indicator_name={self.indicator_name!r}, "
                f"station_code={self.station_code!r}, "
                f"averaging_time={self.averaging_time!r}, "
                f"dates=[{len(self.dates)} dates], "
                f"values=[{len(self.values)} values], "
                f"unit={self.unit!r})")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimeSeries):
            return False
        return (self.indicator_name == other.indicator_name and
                self.station_code == other.station_code and
                self.averaging_time == other.averaging_time)

    def __getitem__(self, key: Union[int, slice, datetime, date]) -> Union[
        Tuple[datetime, float], List[Tuple[datetime, float]], float]:
        # indeks lub slice
        if isinstance(key, int):
            single_date: datetime = self.dates[key]
            raw_value = self.values[key]
            single_value: float = float(raw_value)
            return single_date, single_value

        if isinstance(key, slice):
            dates_list: List[datetime] = self.dates[key]
            raw_values: np.ndarray = self.values[key]
            values_list: List[float] = raw_values.tolist()
            return list(zip(dates_list, values_list))

        # datetime albo date
        if isinstance(key, datetime) or isinstance(key, date):
            for dt, val in zip(self.dates, self.values):
                if isinstance(key, datetime) and dt == key:
                    return float(val)
                if isinstance(key, date) and dt.date() == key:
                    return float(val)
            raise KeyError(f"No measurement found for date {key}")

        # nieobsługiwany typ klucza
        raise TypeError(f"Invalid key type: {type(key)}. Must be int, slice, or datetime/date.")

    # Method requires dataFrame, index of columns with values and unit of measurements
    @classmethod
    def load_ts_from_dataframe(cls, df: pd.DataFrame, index: int, unit: str) -> 'TimeSeries':
        if index == 0:
            raise KeyError("Index zero contains Timestamp, cannot create TimeSeries")

        parts: list[str] = df.columns[index].split('-')
        return cls(
            indicator_name=parts[1],
            station_code=parts[0],
            averaging_time=parts[2],
            dates=df.iloc[:, 0].tolist(),
            values=df.iloc[:, index].tolist(),
            unit=unit
        )

    @property
    def mean(self) -> float:
        clean_arr: np.ndarray = self.values[~np.isnan(self.values)]
        return clean_arr.mean()

    @property
    def std(self) -> float:
        clean_arr: np.ndarray = self.values[~np.isnan(self.values)]
        return clean_arr.std()
