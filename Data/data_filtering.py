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
import statistics

from data_collection import OneMonthData
import datetime


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
    with "garbage" instance attribute values. This filtration should not be
    turned off, and should always be run first.

    Return the list of objects removed.
    """
    # Remove impossible negative values, mostly.
    removed_objects = []

    for data_piece in raw_data:
        data_piece_attributes = vars(data_piece)
        if not all((type(data_piece_attributes[x] is datetime.datetime
                         or data_piece_attributes[x] >= 0 for x in vars(data_piece)))):
            raw_data.remove(data_piece)
            removed_objects.append(data_piece)

    return removed_objects


# TODO: the system is fundamentally not set up for missing values.
# Whoops.
# def filter_missing_data(raw_data: list[OneMonthData]):

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
