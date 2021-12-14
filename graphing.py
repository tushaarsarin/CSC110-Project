import matplotlib.pyplot as plt
import data_collection


def getdata(data: list[data_collection.OneMonthData], include: list[str]) -> list[[]]:
    data_so_far = []
    for i in include:
        data_so_far.append(getattr(obj, i) for obj in data)
    return data_so_far


def gettitle(items: list[str]) -> str:
    title = 'Date'
    for i in range(0, len(items)):
        title += 'VS. ' + items[i]
    return title


def generategraph(data: list[data_collection.OneMonthData], include: list[str]) -> None:
    """
    Creates a scatter plot graph given the data and 2 values to include on X and Y axis
        Preconditions
            - every item in include is a valid attribute of OneMonthData
            - style is a valid pyplot font
    """
    x = [obj.date for obj in data]
    y = getdata(data, include)
    title = gettitle(include)
    plt.title(title)
    plt.style.use('seaborn')
    plt.scatter(x, y, s=150, c='blue')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()




