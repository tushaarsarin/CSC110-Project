import matplotlib.pyplot as plt
from data_collection import OneMonthData
from random import random


def get_data(data: list[OneMonthData], categories_to_plot: list[str]) -> tuple[list[int], list[int]]:
    values = {}
    for category in categories_to_plot:
        values[category] = (list(), list())
        for one_month_data in data:
            values[category][0].append(getattr(one_month_data, category))
            values[category][1].append(one_month_data.date.month)

    return values


def generate_graph(data: list[OneMonthData], categories_to_plot: list[str]) -> None:
    """Creates a scatter plot graph of the categories in categories_to_plot using the data in data."""
    filtered_data = get_data(data, categories_to_plot)
    title = ', '.join(categories_to_plot)
    plt.style.use('seaborn')
    for category in filtered_data:
        plt.scatter(filtered_data[category][0], filtered_data[category][1], s=300, c=((random(), random(), random()),), marker='X')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()




