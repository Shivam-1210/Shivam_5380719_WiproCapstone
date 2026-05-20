import pytest
from utils.excel_reader import read_excel_data

test_data = read_excel_data("PositiveFlights")


@pytest.mark.parametrize(
    "from_city,to_city,departure_date,return_date,passengers,expected_result",
    test_data
)
def test_excel_data_loaded(from_city, to_city, departure_date, return_date, passengers, expected_result):
    assert from_city is not None
    assert to_city is not None
    assert passengers is not None