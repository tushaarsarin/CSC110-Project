import matplotlib.pyplot as plt
import data_collection
import matplotlib.image as img


def getdata(data: list[data_collection.OneMonthData], include: list[str]) -> list[[]]:
    x_data_so_far = []
    y_data_so_far = []
    if 'passengers_can_us_int' in include:
        x_data_so_far.append([obj.passengers_can_not_us for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'passengers_can_not_us' in include:
        x_data_so_far.append([obj.passengers_can_us_int for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'freight_can_us_vehicles' in include:
        x_data_so_far.append([obj.freight_can_us_vehicles for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'freight_intl_teu' in include:
        x_data_so_far.append([obj.freight_intl_teu for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'export_cash' in include:
        x_data_so_far.append([obj.export_cash for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'import_cash' in include:
        x_data_so_far.append([obj.import_cash for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'overall_air_passengers' in include:
        x_data_so_far.append([obj.overall_air_passengers for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    if 'overall_rail_passengers' in include:
        x_data_so_far.append([obj.overall_rail_passengers for obj in data])
        y_data_so_far.append([obj.date.month for obj in data])
    y_data_to_months = []
    for i in y_data_so_far:
        for j in i:
            if j == 1:
                y_data_to_months.append('Jan')
            elif j == 2:
                y_data_to_months.append('Feb')
            elif j ==3:
                y_data_to_months.append('Mar')
            elif j == 4:
                y_data_to_months.append('Apr')
            elif j == 5:
                y_data_to_months.append('May')
            elif j == 6:
                y_data_to_months.append('Jun')
            elif j == 7:
                y_data_to_months.append('Jul')
            elif j == 8:
                y_data_to_months.append('Aug')
            elif j == 9:
                y_data_to_months.append('Sept')
            elif j == 10:
                y_data_to_months.append('Oct')
            elif j == 11:
                y_data_to_months.append('Nov')
            elif j == 12:
                y_data_to_months.append('Dec')
            else:
                return 'Something messed up'
    return [x_data_so_far, y_data_to_months]


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
    print(fitered_data[1])
    plt.scatter(fitered_data[1], fitered_data[0], s=300, c=color, marker=marker)
    plt.xlabel('Date')
    plt.ylabel('Value')
    dollar_marker = img.imread('img/cash.png')
    train_marker = img.imread('img/train.png')
    transport_marker = img.imread('img/car.png')
    plt.show()




