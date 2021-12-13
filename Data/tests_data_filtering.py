# In this file are tests, and functions who support testing.
import unittest
import data_filtering
from data_collection import OneMonthData
import hypothesis.strategies
from hypothesis import strategies


# Hypothesis has no OneMonthData strategy... bah! Improvisation time!
def generate_random_data(quantity: int) -> list[OneMonthData]:
    """Randomly generate -quantity- OneMonthData objects, with random
    attributes for property based testing.

    Not completely random but will provide decent variance.
    """
    import random
    # Accumulates constructed data objects.
    data_so_far = []

    int_to_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                    5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
                    10: 'October', 11: 'November', 12: 'December'}
    for i in range(0, quantity):
        random_month = int_to_month[random.randint(1, 12)]
        # For convenience, we restrict the random day range to not have to deal
        # with leap years and smaller months etc.
        random_year = random.randint(1984, 2022)
        random_pass_can_us_int = random.randint(-100, 1000)
        random_pass_can_not_us = random.randint(-100, 1000)
        random_freight_can_us_vehicles = random.randint(-100, 1000)
        random_freight_intl_teu = random.randint(-100, 1000)
        random_export_cash = random.randint(-100, 1000)
        random_import_cash = random.randint(-100, 1000)
        random_overall_air_passengers = random.randint(-100, 1000)
        random_overall_rail_passengers = random.randint(-100, 1000)

        current_object = OneMonthData(random_month, random_year,
                                      random_pass_can_us_int, random_pass_can_not_us,
                                      random_freight_can_us_vehicles,
                                      random_freight_intl_teu, random_export_cash,
                                      random_import_cash, random_overall_air_passengers,
                                      random_overall_rail_passengers)
        data_so_far.append(current_object)
        return data_so_far


def test_no_lost_data() -> None:
    """Test that each of the filtering helpers do not lose elements somehow,
    e.g. filtered_elements + raw_data list after = raw_data list before."""

    raw_data = generate_random_data(1000)
    previous_raw_data = raw_data + []
    assert previous_raw_data == \
           data_filtering.filter_garbage_values(raw_data) + raw_data

    raw_data = generate_random_data(1000)
    previous_raw_data = raw_data + []
    assert previous_raw_data == \
           data_filtering.filter_duplicate_data(raw_data) + raw_data

    raw_data = generate_random_data(1000)
    previous_raw_data = raw_data + []

    # Get each instance attribute. Plug that one in as the value.
    instance_attributes = [x for x in dir(OneMonthData) if not
    callable(getattr(OneMonthData, x)) and not x.startswith('_')]

    for attribute in instance_attributes:
        assert previous_raw_data == \
               data_filtering.filter_outlying_value(raw_data, attribute) + raw_data


def test_no_duplicates() -> None:
    """Test that the duplicate filtering function, when given a list of random
    OneMonthData objects, mutates the list into one with no duplicates.
    """
    raw_data = generate_random_data(1000)
    data_filtering.filter_duplicate_data(raw_data)
    appearance_count = {}
    for x in raw_data:
        if x not in appearance_count:
            appearance_count[x] = 0
        appearance_count[x] += 1

    assert all((appearance_count[x] <= 1 for x in appearance_count))


def test_no_garbage() -> None:
    """Test that the garbage filtering function, when given a list of random
    OneMonthData objects, mutates the list into one with no garbage.
    """
    import datetime

    raw_data = generate_random_data(1000)
    data_filtering.filter_garbage_values(raw_data)
    assert all((data_filtering.earliest_yr_in_dataset <= entry.date.year
                <= data_filtering.latest_yr_in_dataset
                for entry in raw_data))

    for entry in raw_data:
        data_piece_attributes = vars(entry)
        assert all((type(data_piece_attributes[x] is datetime.datetime
                         or data_piece_attributes[x] >= 0 for x in vars(entry))))

def test_no_outliers() -> None:
    """Test that the outlier filtering function, when given a list of random
    OneMonthData objects, mutates the list into one with no objects that
    have outlying values.
    """
    import statistics

    raw_data = generate_random_data(1000)
    for value_name in dir(OneMonthData):
        # Ignore precondition-defying values, and system specials and private
        # attributes.
        if value_name != 'date' and not value_name.startswith('_'):
            # Generate a list of the value in question from all the OneMonthData values.
            value_list_number_only = [getattr(bit, value_name) for bit in raw_data]
            # Sort the list. Compute IQR, Q1, and Q3.
            value_list_number_only = sorted(value_list_number_only)
            quantiles = statistics.quantiles(data=value_list_number_only, n=4,
                                             method='inclusive')
            q1 = quantiles[0]
            q3 = quantiles[2]
            iqr = q3 - q1
            data_filtering.filter_outlying_value(raw_data, value_name)
            # Now check that there are no values of that value that are outliers.
            for element in raw_data:
                assert not data_filtering.is_outlier(getattr(element, value_name), q1,
                                                     q3, iqr)

def test_statistical_attributes_uniform_input() -> None:
    """Unit test for statistical attributes with a uniform input."""
    expected = {'mean': 5000000.0, 'mode': 5000000.0, 'median': 5000000.0, 'standard deviation': 0.0}
    object1 = OneMonthData('January', 2021, 5, 5, 5, 5, 5, 5, 5, 5)
    object2 = OneMonthData('February', 2021, 5, 5, 5, 5, 5, 5, 5, 5)

    # The function behaviour generalizes for all values. So it should be safe to just test one.
    test_list = [object1, object2]
    assert data_filtering.calculate_aggregate_measurements(test_list, 'export_cash') == expected

def test_statistical_attributes_not_uniform_input() -> None:
    """Unit test for statistical attributes with a non-uniform input."""
    expected = {'mean': 2500000.0, 'mode': 5000000.0, 'median': 2500000.0, 'standard deviation': 2500000.0}
    object1 = OneMonthData('January', 2021, 5, 5, 5, 5, 5, 5, 5, 5)
    object2 = OneMonthData('February', 2021, 0, 0, 0, 0, 0, 0, 0, 0)

    # The function behaviour generalizes for all values. So it should be safe to just test one.
    test_list = [object1, object2]
    assert data_filtering.calculate_aggregate_measurements(test_list, 'export_cash') == expected

if __name__ == '__main__':
    pass
    # whatever I decide to put in the main block.