import matplotlib.pyplot as plt
import data_collection
import matplotlib.image as img


def getdata(data: list[data_collection.OneMonthData], include: list[str]) -> list[[]]:
    x_data_so_far = []
    y_data_so_far = []
    passengers_can_us_int: int
    passengers_can_not_us: int
    freight_can_us_vehicles: int
    freight_intl_teu: float
    export_cash: float
    import_cash: float
    overall_air_passengers: int
    overall_rail_passengers: int
    for i in data:
        if 'passengers_can_us_int' in include:
            x_data_so_far.append(i.passengers_can_not_us)
            y_data_so_far.append(i.date.month)
        if 'passengers_can_not_us' in include:
            x_data_so_far.append(i.passengers_can_us_int)
            y_data_so_far.append(i.date.month)
        if 'freight_can_us_vehicles' in include:
            x_data_so_far.append(i.freight_can_us_vehicles)
            y_data_so_far.append(i.date.month)
        if 'freight_intl_teu' in include:
            x_data_so_far.append(i.freight_intl_teu)
            y_data_so_far.append(i.date.month)
        if 'export_cash' in include:
            x_data_so_far.append(i.export_cash)
            y_data_so_far.append(i.date.month)
        if 'import_cash' in include:
            x_data_so_far.append(i.import_cash)
            y_data_so_far.append(i.date.month)
        if 'overall_air_passengers' in include:
            x_data_so_far.append(i.overall_air_passengers)
            y_data_so_far.append(i.date.month)
        if 'overall_rail_passengers' in include:
            x_data_so_far.append(i.overall_rail_passengers)
            y_data_so_far.append(i.date.month)
    return [x_data_so_far, y_data_so_far]


def gettitle(items: list[str]) -> str:
    title = 'Date '
    for i in range(0, len(items)):
        title += ' VS. ' + items[i]
    return title

def generategraph(data: list[data_collection.OneMonthData], include: list[str]) -> None:
    """
    Creates a scatter plot graph given the data and 2 values to include on X and Y axis
        Preconditions
            - every item in include is a valid attribute of OneMonthData
            - style is a valid pyplot font
    """
    fitered_data = getdata(data, include)
    title = gettitle(include)
    plt.title(title)
    marker = 'X'
    color = 'blue'
    if 'import_cash' in include or 'export_cash' in include:
       color = 'green'
    plt.style.use('seaborn')
    plt.scatter(fitered_data[0], fitered_data[1], s=300, c=color, marker=marker)
    plt.xlabel('Date')
    plt.ylabel('Value')
    dollar_marker = img.imread('img/cash.png')
    train_marker = img.imread('img/train.png')
    transport_marker = img.imread('img/car.png')
    plt.show()




