import math

import matplotlib.pyplot as plt
from matplotlib import pyplot
import data_collection

def getdata(data: list[data_collection.OneMonthData], include: list[str]) -> list[[]]:
    data_so_far = []
    for i in include:
        data_so_far.append([getattr(obj, i) for obj in data])
    return data_so_far


def gettitle(items: list[str]) -> str:
    title = items[0]
    for i in range(1,len(items)):
        title += 'VS. ' + items[i]
    return title


def generategraph(data: list[data_collection.OneMonthData], include: list[str]) -> None:
    """
    Creates a scatter plot graph given the data and 2 values to include on X and Y axis
        Preconditions
            - every item in include is a valid attribute of OneMonthData
            - style is a valid pyplot font
    """
    title = gettitle(include)
    data_to_graph = getdata(data, include)
    pyplot.title(title)
    plt.xlabel('Time')
    plt.ylabel('Value')
    pyplot.plot(data_to_graph, loc='lower right')
    pyplot.legend(include)
    plt.show()

