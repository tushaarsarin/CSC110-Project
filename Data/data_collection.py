# The purpose of this file is primarily to collect and organize raw data.
# Could put filtering here too but for the moment I'm keeping it full of data
# organizational stuff.
import csv
from dataclasses import dataclass
from datetime import datetime

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
        - date is a valid date
        - all(x >= 0 for x in [passengers_can_us_int, passengers_can_not_us,
        freight_can_us_vehicles, freight_intl_teu, export_cash, import_cash
        overall_air_passengers, overall_rail_passengers])

    Note: the dataset does not specify a day - we use a default value of 1
    but this is vacuous.

    """
    date: datetime
    passengers_can_us_int: int
    passengers_can_not_us: int
    freight_can_us_vehicles: int
    freight_intl_teu: int
    export_cash: int
    import_cash: int
    overall_air_passengers: int
    overall_rail_passengers: int

    # Private attributes:
    # _month_to_int: maps month as a string to an integer.
    _month_to_int = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                     'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
                     'October': 10, 'November': 11, 'December': 12}

    def __init__(self, month: str, year: int, passengers_can_us_int: int,
                 passengers_can_not_us: int, freight_can_us_vehicles: int,
                 freight_intl_teu: int, export_cash: int, import_cash: int,
                 overall_air_passengers: int, overall_rail_passengers: int):
        """Initialize the instance attributes and perform some
        basic multiplications - because the raw data is scaled down relative
        to actual values.

        Convert components to a date here for user convenience.
        """
        # Magic number clarification: most data values are scaled up by 1000.
        # Cash values are scaled down by 1 mil in the dataset. We want raw.
        self.date = datetime(year, self._month_to_int[month], 1)
        self.passengers_can_us_int = passengers_can_not_us * 1000
        self.passengers_can_not_us = passengers_can_us_int * 1000
        self.freight_can_us_vehicles = freight_can_us_vehicles * 1000
        self.freight_intl_teu = freight_intl_teu * 1000

        # python int is quite big so this should still fit.
        self.export_cash = export_cash * 1000000
        self.import_cash = import_cash * 1000000

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


    >>> process_file(r'TestData.csv')
    """
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
                  data[12][col], data[13][col], data[14][col], data[17][col],
                  data[18][col], data[20][col], data[21][col]]

        if not any((value is None for value in values)):
            current_month_data = OneMonthData(
                month=date_str.split()[0],
                year=int(date_str.split()[1]),
                passengers_can_us_int=int(data[11][col]),
                passengers_can_not_us=int(data[12][col]),
                freight_can_us_vehicles=int(data[13][col]),
                freight_intl_teu=int(data[14][col]),
                export_cash=int(data[17][col]),
                import_cash=int(data[18][col]),
                overall_air_passengers=int(data[20][col]),
                overall_rail_passengers=int(data[21][col])
            )
            data_so_far.append(current_month_data)

    return data_so_far

if __name__ == '__main__':
    pass
    # Whatever I decide to put in the main block.
