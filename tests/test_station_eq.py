from src.station import Station

def create_station(code: str) -> Station:
    return Station(
        station_code=code,
        international_code="INT001",
        station_name="StationName",
        old_name="OldStation",
        launch_date="2000-01-01",
        close_date="",
        station_type="TypeA",
        area_type="Urban",
        type_of_station="Traffic",
        voivodeship="Mazowieckie",
        town="Warszawa",
        address="Main Street 1",
        latitude_n="52.2297",
        longitude_e="21.0122"
    )

def test_station_eq_same_code():
    station1 = create_station("ABC123")
    station2 = create_station("ABC123")
    assert station1 == station2, "Stations with the same code should be equal"

def test_station_eq_different_code():
    station1 = create_station("ABC123")
    station2 = create_station("XYZ789")
    assert station1 != station2, "Stations with different codes should not be equal"

def test_station_eq_different_type():
    station = create_station("ABC123")
    not_a_station = "ABC123"
    assert station != not_a_station, "Station should not be equal to a non-Station object"
