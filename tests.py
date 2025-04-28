from datetime import datetime, date

from data_parser import parse_metafile, parse_measures
from series_validator import OutlierDetector, CompositeValidator, ZeroSpikeDetector, ThresholdDetector
from station import Station
from time_series import TimeSeries


def station_test():
    df = parse_metafile('data_S5/stacje.csv')

    station1 = Station.from_dataframe_row(df.iloc[1])

    print(station1)

def time_series_test():
    df, unit = parse_measures('data_S5/measurements/2023_CO_1g.csv')

    time_series1 = TimeSeries.from_dataframe(df,1,unit)

    print(time_series1)
    print(f'Standard deviation of values: {time_series1.std}')
    print(f'Mean of values: {time_series1.mean}')
    print(time_series1[1])
    print(time_series1[2:5])
    #print(time_series1[datetime(2023, 1, 8)])
    print(time_series1[datetime(2023, 1, 1, 1)])
    print(time_series1[date(2023, 1, 1)])

def series_validator_test():
    df, unit = parse_measures('data_S5/measurements/2023_PM10_24g.csv')

    time_series1 = TimeSeries.from_dataframe(df, 2, unit)
    time_series2 = TimeSeries.from_dataframe(df, 4, unit)

    time_series = [time_series1, time_series2]

    series_validator1 = OutlierDetector(2)
    series_validator2 = ZeroSpikeDetector()
    series_validator3 = ThresholdDetector(50)
    series_validator4 = CompositeValidator(validators=[series_validator1, series_validator2, series_validator3], mode='AND')
    series_validator5 = CompositeValidator(validators=[series_validator1, series_validator2, series_validator3], mode='OR')

    series_validators = [series_validator1, series_validator2, series_validator3, series_validator4, series_validator5]

    for time_series in time_series:
        for series_validator in series_validators:
            print(series_validator.analyze(time_series))

        print()

if __name__ == '__main__':
    #station_test()
    #time_series_test()
    series_validator_test()