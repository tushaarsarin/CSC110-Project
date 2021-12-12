# The purpose of this file is to handle the filtration and cleaning of any
# and all "garbage" data that we find - if we find it.
# Garbage data refers to OneMonthData objects with nonsensical values, e.g.
# -999,999,999 travellers, or something like that.

# Architecture:
# Large filtration function "manager"
# Rely on a bunch of small helpers that filter based off of a specific thing.
# That way the user we can tick on or off certain filter types.
# Should try to have aggregate kinda data available.
# That way if an MF wants to keep non-missing values in aggregate, they can.
# However, graphing with missing and garbo values does not make sense.
import math
import statistics
from typing import Optional

from data_collection import OneMonthData
import datetime

earliest_yr_in_dataset = 2017
latest_yr_in_dataset = 2021


def calculate_aggregate_measurements(data: list[OneMonthData], value: str) \
        -> dict[str, float]:
    """Calculate some aggregate statistical measurements on filtered data, for
    some particular measurement.

    Return a dictionary mapping measurement name to its value.

    Statistical measurements are: mean, mode, median, standard deviation.

    Preconditions:
    - data has been filtered, if appropriate.
    """
    # TODO: some of these could be helpers, low key.
    statistical_measurements = {}
    values = [getattr(x, value) for x in data]
    # calculate mean by summing and dividing.
    statistical_measurements['mean'] = sum(values) \
                                       / len(values)

    # maps values to the number of times they occur.
    values_to_occurrences = {}
    for element in values:
        if element not in values_to_occurrences:
            values_to_occurrences[element] = 0
        values_to_occurrences[element] += 1

    # accumulator for the most common value so far (with occurrences)
    most_common_value_so_far = [-1, -1]
    for element in values_to_occurrences:
        if values_to_occurrences[element] > most_common_value_so_far[1]:
            most_common_value_so_far[0] = value
            most_common_value_so_far[1] = values_to_occurrences[element]

    statistical_measurements['mode'] = most_common_value_so_far[0]

    # Sort the list and then apply the formula to get median.
    values = sorted(values)
    if len(values) % 2 == 0:
        statistical_measurements['median'] = values[len(values) // 2]
    else:
        statistical_measurements['median'] = (values[(len(values) - 1) // 2]
                                              + values[(len(values) + 1) // 2]) / 2

    sigma_value_minus_mean = sum([value - statistical_measurements['mean'] for
                              value in values])
    statistical_measurements['standard deviation'] = \
        math.sqrt(sigma_value_minus_mean ** 2 / len(values))

    return  statistical_measurements

def filter(filter_garbage: bool, filter_duplicates: bool,
           values_to_filter_outliers_for: list[str], raw_data: list[OneMonthData]) \
        -> list[OneMonthData]:
    """Filter according to instructions given as arguments.
    Mutate the raw_data according to the arguments given.
    To filter no outliers, keep the list empty.

    Return a list of all filtered elements.

    Preconditions:
    - values_to_filter_outliers_for should consist only of valid value names.
    """
    filtered_values = []
    if filter_garbage:
        filtered_values.extend(filter_garbage_values(raw_data))

    if filter_duplicates:
        filtered_values.extend(filter_duplicate_data(raw_data))

    for value in values_to_filter_outliers_for:
        filtered_values.extend(filter_outlying_value(raw_data, value))

    return filtered_values


def filter_garbage_values(raw_data: list[OneMonthData]) \
        -> list[OneMonthData]:
    """Mutate a list of OneMonthData objects, removing any objects
    with "garbage" instance attribute values.
    Return the list of objects removed.

    We recommend that this filtration not be
    turned off, and always be run first. Though we leave the option to
    the user.
    """
    # Remove impossible negative values, mostly.
    removed_objects = []

    for data_piece in raw_data:
        data_piece_attributes = vars(data_piece)
        if not all(
                (type(data_piece_attributes[x]) is datetime.datetime
                         or data_piece_attributes[x] >= 0 for x in vars(data_piece))

        ):
            raw_data.remove(data_piece)
            removed_objects.append(data_piece)

    # Also, remove objects with impossible dates (year)
    for data_piece in raw_data:
        if latest_yr_in_dataset < data_piece.date.year < earliest_yr_in_dataset:
            raw_data.remove(data_piece)
            removed_objects.append(data_piece)

    return removed_objects


def filter_duplicate_data(raw_data: list[OneMonthData]):
    """Mutate a list of OneMonthData objects, to remove duplicate objects.
    A duplicate object is one that is completely identical to another one, in all
    respects. Return a list of culled duplicate objects.

    If, for some reason, duplicate data is permissible, this can be skipped.
    """
    unique_values = set(raw_data)
    # Vacuous re-assignment to break aliasing
    value_copy_raw_data_list = raw_data + []
    # Get non-unique values.
    # unique_values should be within value_copy_raw_data_list.
    for value in unique_values:
        value_copy_raw_data_list.remove(value)

    for duplicate in value_copy_raw_data_list:
        raw_data.remove(duplicate)
    return value_copy_raw_data_list


def filter_outlying_value(raw_data: list[OneMonthData], value_name: str) \
        -> list[OneMonthData]:
    """
    Mutate raw_data to remove entries that include a statistically outlying
    value of some value. Return a list of removed entries.

    Note that this will artificially smoothen the data because outliers are
    removed indiscriminately and without justification.

    Preconditions:
    - value_name != 'date'
    """
    # Generate a list of the value in question from all the OneMonthData values.
    value_list_number_only = [getattr(bit, value_name) for bit in raw_data]
    # Sort the list. Compute IQR, Q1, and Q3.
    value_list_number_only = sorted(value_list_number_only)
    quantiles = statistics.quantiles(data=value_list_number_only, n=4,
                                     method='inclusive')
    q1 = quantiles[0]
    q3 = quantiles[2]
    iqr = q3 - q1
    # Iterate through all values and cull entries w/ outliers.
    value_list = [(getattr(bit, value_name), bit) for bit in raw_data]
    removed_entries = []
    for value in value_list:
        if is_outlier(value[0], q1, q3, iqr):
            raw_data.remove(value[1])
            removed_entries.append(value[1])
    return removed_entries


def is_outlier(value: int, q1: int, q3: int, iqr: int) -> bool:
    """Return whether a given value is an outlying one, based off of quantile
    measurements.
    """
    return value > 1.5 * iqr + q3 or value < q1 - 1.5 * iqr


if __name__ == '__main__':
    pass
    # whatever I decide to put into the main block.
