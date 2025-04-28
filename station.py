class Station:
    def __init__(self, station_code, international_code, station_name, old_name, launch_date, close_date, station_type,
                 area_type, type_of_station, voivodeship, town, address, latitude_n, longitude_e):
        self.station_code = station_code
        self.international_code = international_code
        self.station_name = station_name
        self.old_name = old_name
        self.launch_date = launch_date
        self.close_date = close_date
        self.station_type = station_type
        self.area_type = area_type
        self.type_of_station = type_of_station
        self.voivodeship = voivodeship
        self.town = town
        self.address = address
        self.latitude_n = latitude_n
        self.longitude_e = longitude_e

    def __str__(self):
        return f'Station code: {self.station_code}, Station name: {self.station_name}'

    def __repr__(self):
        return (
            f"Station(station_code={self.station_code!r}, international_code={self.international_code!r}, "
            f"station_name={self.station_name!r}, old_name={self.old_name!r}, launch_date={self.launch_date!r}, "
            f"close_date={self.close_date!r}, station_type={self.station_type!r}, area_type={self.area_type!r}, "
            f"type_of_station={self.type_of_station!r}, voivodeship={self.voivodeship!r}, town={self.town!r}, "
            f"address={self.address!r}, latitude_n={self.latitude_n!r}, longitude_e={self.longitude_e!r})")

    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.station_code == other.station_code

    @classmethod
    def from_dataframe_row(cls, row):
        return cls(
            station_code=row["Kod stacji"],
            international_code=row["Kod międzynarodowy"],
            station_name=row["Nazwa stacji"],
            old_name=row["Stary Kod stacji \r\n(o ile inny od aktualnego)"],
            launch_date=row["Data uruchomienia"],
            close_date=row["Data zamknięcia"],
            station_type=row["Typ stacji"],
            area_type=row["Typ obszaru"],
            type_of_station=row["Rodzaj stacji"],
            voivodeship=row["Województwo"],
            town=row["Miejscowość"],
            address=row["Adres"],
            latitude_n=row["WGS84 φ N"],
            longitude_e=row["WGS84 λ E"]
        )
