import abc
from typing import List

import numpy as np

from time_series import TimeSeries


class SeriesValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def analyze(self, series: TimeSeries):
        """Returns communicates describing detected anomalies
        or empty list, if no anomalies were detected"""
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k):
        self.k = k

    def analyze(self, series):
        mean = series.mean
        std = series.std

        outliers = []

        for date, value in zip(series.dates, series.values):
            if value is not None and abs(value - mean) > self.k * std:
                outliers.append((date,value))

        return [f"Outlier detected at {date}: value={value}" for (date, value) in outliers]

class ZeroSpikeDetector(SeriesValidator):
    def __init__(self, num_of_zeroes = 3):
        self.num_of_zeroes = num_of_zeroes

    def analyze(self, series):
        anomalies = []
        count = 0
        start_date = None
        end_date = None

        for date, value in zip(series.dates, series.values):
            if np.isnan(value) or value == 0:
                if count == 0:
                    start_date = date
                end_date = date
                count += 1
            else:
                if count >= self.num_of_zeroes:
                    anomalies.append(f"Zero spike detected starting at {start_date} and ended at {end_date}")
                count = 0
                start_date = None
                end_date = None

        if count >= self.num_of_zeroes:
            anomalies.append(f"Zero spike detected starting at {start_date} and ended at {end_date}")

        return anomalies


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold):
        self.threshold = threshold

    def analyze(self, series):
        anomalies = []

        for date, value in zip(series.dates, series.values):
            if value > self.threshold:
                anomalies.append(f"Threshold exceeded at {date} with value {value}")

        return anomalies

class CompositeValidator(SeriesValidator):
    def __init__(self, validators: List[SeriesValidator], mode: str):
        self.validators = validators
        self.mode = mode

    def analyze(self, series):
        all_messages = []
        has_issues_flags = []

        # Zbieramy komunikaty osobno dla każdego walidatora
        for validator in self.validators:
            messages = validator.analyze(series)
            has_issues_flags.append(bool(messages))
            all_messages.extend(messages)

        if self.mode == "AND":
            # AND: wszystkie walidatory muszą zwrócić przynajmniej jeden komunikat
            if all(has_issues_flags):
                return all_messages
            else:
                return []

        elif self.mode == "OR":
            # OR: przynajmniej jeden walidator musi zwrócić komunikaty
            if any(has_issues_flags):
                return all_messages
            else:
                return []

        else:
            raise ValueError("Invalid mode. Use 'AND' or 'OR'.")