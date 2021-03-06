"""CSC110 Project Phase 2

FILE DESCRIPTION
================
This file collects raw data and organizes it into OneMonthData objects.

GROUP INFORMATION
=================
Tushaar Sarin, Michael Yu, Parshwa Gada, Rohan Sahota
"""
import csv
from dataclasses import dataclass
from datetime import datetime

class BadMonthError(Exception):
    """An exception for when we attempt to make a malformed date-datetime
    object with an invalid month. Due to the way date-datetime works
    we can't actually just make a malformed one and allow the user the choice
    of keeping it in or filter it out later.
    """

    def __str__(self):
        return 'Invalid month encountered when attempting to' \
               'construct data.'

class OneMonthData:
    """A dataclass to store about a month's worth of data from the
    transportation activity dataset.

    passengers_can_us_int: International passengers,
    number of Canadian and U.S. travellers between Canada
    and the United States (x 1,000)

    passengers_can_not_us:  International passengers,
    number of Canadian and non-U.S. travellers
    overseas, all modes of transport (x 1,000)

    freight_can_us:  International freight, number of commercial vehicles
    travelling between Canada and the United States (x 1,000)

    freight_intl_teu: International freight, total twenty-foot equivalent units
    (TEUs) handled at four major container ports (x 1,000)

    export_cash: Merchandise trade, total export of goods (x 1,000,000)

    import_cash: Merchandise trade, total import of goods (x 1,000,000)

    overall_air_passengers: Domestic and international passengers, air
    (x 1,000)

    overall_rail_passengers: Domestic and international passengers,
    rail (VIA Rail) (x 1,000)

    Representation Invariants:
        - month is a valid month


    Note: the dataset does not specify a day - we use a default value of 1
    but this is vacuous.

    """
    date: datetime
    passengers_can_us_int: int
    passengers_can_not_us: int
    freight_can_us_vehicles: int
    freight_intl_teu: float
    export_cash: float
    import_cash: float
    overall_air_passengers: int
    overall_rail_passengers: int

    # Private attributes:
    # _month_to_int: maps month as a string to an integer.
    _month_to_int = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                     'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
                     'October': 10, 'November': 11, 'December': 12}

    def __init__(self, month: str, year: int, passengers_can_us_int: int,
                 passengers_can_not_us: int, freight_can_us_vehicles: int,
                 freight_intl_teu: float, export_cash: float, import_cash: float,
                 overall_air_passengers: int, overall_rail_passengers: int):
        """Initialize the instance attributes and perform some
        basic multiplications - because the raw data is scaled down relative
        to actual values.

        Convert components to a date here for user convenience.
        """
        # Magic number clarification: most data values are scaled up by 1000.
        # Cash values are scaled down by 1 mil in the dataset. We want raw.
        if month not in self._month_to_int:
            raise BadMonthError

        self.date = datetime(year, self._month_to_int[month], 1)
        self.passengers_can_us_int = passengers_can_us_int * 1000
        self.passengers_can_not_us = passengers_can_not_us * 1000
        self.freight_can_us_vehicles = freight_can_us_vehicles * 1000
        self.freight_intl_teu = freight_intl_teu * 1000.0

        # python int is quite big so this should still fit.
        self.export_cash = export_cash * 1000000.0
        self.import_cash = import_cash * 1000000.0

        self.overall_air_passengers = overall_air_passengers * 1000
        self.overall_rail_passengers = overall_rail_passengers * 1000


def process_file(filename: str) -> list[OneMonthData]:
    """Process a raw .csv from the transportation activity dataset
    into usable and reasonably formatted OneMonthData objects.
    Return a list of them - all of the ones we find in the file.

    Instructions to user: INPUT THE FILE NAME AS A RAW STRING, E.G.
    r'TestData.csv'.

    Preconditions:
    - This python file is in the same directory as the .csv files

    # The comparison will always return false due to a class instance quirk. But, conceptually,
    # this doctest should be satisfied and will help with understanding.
    # (instance attribute values should be the same)
    >>> expected = [OneMonthData('April', 2021, 379, 90, 452, 582.1, 48859, 49683, 572, 45), \
    OneMonthData('May', 2021, 425, 78, 443, 681.0, 49888, 50226, 640, 50), \
    OneMonthData('June', 2021, 439, 96, 474, 569.8, 55219, 51580, 937, 78), \
    OneMonthData('July', 2021, 598, 205, 448, 584.5, 51239, 51007, 1896, 135), \
    OneMonthData('August', 2021, 1016, 433, 456, 621.3, 53764, 52259, 1152, 202)]

    >>> process_file(r'TestData.csv') == expected
    True


    """
    expected = [OneMonthData('April', 2021, 379, 90, 452, 582.1, 48859, 49683, 572, 45),
                OneMonthData('May', 2021, 425, 78, 443, 681.0, 49888, 50226, 640, 50),
                OneMonthData('June', 2021, 439, 96, 474, 569.8, 55219, 51580, 937, 78),
                OneMonthData('July', 2021, 598, 205, 448, 584.5, 51239, 51007, 1896, 135),
                OneMonthData('August', 2021, 1016, 433, 456, 621.3, 53764, 52259, 1152, 202)]

    # Read the file, dump it into a very raw table.
    # Need the UTF-8 encoding or python tries to use binary to decode.
    raw_file = open(filename, encoding='UTF-8')
    reader = csv.reader(raw_file)
    data = [row for row in reader]
    raw_file.close()

    # Iterate over the columns. Manually assign appropriate values into a data
    # class object. Return a list.
    # Accumulator for OneMonthData objects.
    data_so_far = []
    for col in range(1, len(data[8])):
        date_str = data[9][col]
        # Quickly make sure no values are empty - if one is, ignore the object.
        values = [date_str.split()[0], date_str.split()[1], data[11][col],
                  data[12][col], data[13][col], data[15][col], data[17][col],
                  data[18][col], data[20][col], data[21][col]]

        if not any((value == '' for value in values)):
            current_month_data = OneMonthData(
                month=date_str.split()[0],
                year=int(date_str.split()[1]),
                # The dataset uses commas to separate sections of large numbers. They need to be culled.
                passengers_can_us_int=int(data[11][col].replace(',', '')),
                passengers_can_not_us=int(data[12][col].replace(',', '')),
                freight_can_us_vehicles=int(data[13][col].replace(',', '')),
                freight_intl_teu=float(data[15][col].replace(',', '')),
                export_cash=float(data[17][col].replace(',', '')),
                import_cash=float(data[18][col].replace(',', '')),
                overall_air_passengers=int(data[20][col].replace(',', '')),
                overall_rail_passengers=int(data[21][col].replace(',', ''))
            )
            data_so_far.append(current_month_data)

    return data_so_far


if __name__ == '__main__':
    process_file(r'TestData.csv')
