from datetime import datetime, date
import numpy as np


class TimeSeries:
    def __init__(self, indicator_name, station_code, averaging_time, dates, values, unit):
        self.indicator_name = indicator_name  # np. "PM10"
        self.station_code = station_code  # kod stacji
        self.averaging_time = averaging_time  # np. "1h"
        self.dates = dates  # lista obiektów datetime
        self.values = np.array(values)  # tablica numpy wartości (float lub None)
        self.unit = unit  # np. "µg/m³"

    def __str__(self):
        return f'Station code: {self.station_code}, Indicator name: {self.indicator_name}, Averaging time: {self.averaging_time}'

    def __repr__(self):
        return (f"TimeSeries(indicator_name={self.indicator_name!r}, "
                f"station_code={self.station_code!r}, "
                f"averaging_time={self.averaging_time!r}, "
                f"dates=[{len(self.dates)} dates], "
                f"values=[{len(self.values)} values], "
                f"unit={self.unit!r})")

    def __eq__(self, other):
        if not isinstance(other, TimeSeries):
            return False
        return (self.indicator_name == other.indicator_name and
                self.station_code == other.station_code and
                self.averaging_time == other.averaging_time)



    def __getitem__(self, key):
        # Jeśli key to indeks lub slice
        if isinstance(key, int) or isinstance(key, slice):
            result_dates = self.dates[key]
            result_values = self.values[key]
            # Jeśli jeden element (int), zwracamy pojedynczą krotkę
            if isinstance(key, int):
                return result_dates, result_values
            else:
                # Jeśli kilka elementów (slice), zwracamy listę krotek
                return list(zip(result_dates, result_values))

        # Jeśli key to datetime.date lub datetime.datetime
        elif isinstance(key, datetime) or isinstance(key, date):
            for dt, value in zip(self.dates, self.values):
                if isinstance(key, datetime):
                    if dt == key:
                        return value
                else:  # key jest typu date
                    if dt.date() == key:
                        return value
            raise KeyError(f"No measurement found for date {key}")

        else:
            raise TypeError(f"Invalid key type: {type(key)}. Must be int, slice, or datetime/date.")

    # Method requires dataFrame, index of columns with values and unit of measurements
    @classmethod
    def load_ts_from_dataframe(cls, df, index, unit):
        if index == 0:
            raise KeyError("Index zero contains Timestamp, cannot create TimeSeries")

        parts = df.columns[index].split('-')
        return cls(
            indicator_name=parts[1],
            station_code=parts[0],
            averaging_time=parts[2],
            dates=df.iloc[:, 0].tolist(),
            values=df.iloc[:, index].tolist(),
            unit=unit
        )

    @property
    def mean(self):
        clean_arr = self.values[~np.isnan(self.values)]
        return clean_arr.mean()

    @property
    def std(self):
        clean_arr = self.values[~np.isnan(self.values)]
        return clean_arr.std()