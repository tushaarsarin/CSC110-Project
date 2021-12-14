"""CSC110 Project Phase 2

FILE DESCRIPTION
================
This file renders the main window for the program.
It provides an interface for the elements and options defined in other files.

GROUP INFORMATION
=================
Tushaar Sarin, Michael Yu, Parshwa Gada, Rohan Sahota
"""
import tkinter as tk
from dataclasses import dataclass

from data_collection import OneMonthData, process_file
from data_filtering import filter
import graphing


@dataclass
class CSProject:
    """Renders the main window for the Project."""
    data: list[OneMonthData]
    categories_to_plot: list[str]
    categories_to_filter: list[str]
    additional_filters: list[str]
    _window: tk.Tk
    _frame_categories: tk.LabelFrame
    _frame_filters: tk.LabelFrame
    update_graph_btn: tk.Button
    category_to_value: dict[str, tk.IntVar]
    category_to_checkbox: dict[str, tk.Checkbutton]
    filter_to_value: dict[str, tk.IntVar]
    filter_to_checkbox: dict[str, tk.Checkbutton]
    additional_filter_to_value: dict[str, tk.IntVar]
    additional_filter_to_checkbox: dict[str, tk.Checkbutton]

    def __init__(self, title: str = 'Title', dimensions: tuple[int, int] = (1280, 720), offset: tuple[int, int] = None):
        # main window:
        ################################################################################################################
        self._window = tk.Tk()
        self._window.title(title)
        self.position_window(dimensions, offset)
        ################################################################################################################

        # frame objects:
        ################################################################################################################
        self._frame_categories = tk.LabelFrame(self._window, text='Data Categories', padx=5, pady=5)
        self._frame_categories.grid(row=0, column=0, padx=10, pady=10)

        self._frame_filters = tk.LabelFrame(self._window, text='Outlier Filtration Options', padx=5, pady=5)
        self._frame_filters.grid(row=1, column=0, padx=10, pady=10)
        ################################################################################################################

        self.render_category_options()
        self.render_filter_options()

        self.load_default_categories()

    def position_window(self, dimensions: tuple[int, int], offset: tuple[int, int]) -> None:
        """Position the window on-screen."""
        window_width, window_height = dimensions
        if not offset:
            screen_width, screen_height = self._window.winfo_screenwidth(), self._window.winfo_screenheight()
            x, y = (screen_width // 2) - (window_width // 2), (screen_height // 2) - (window_height // 2)
        else:
            x, y, = offset
        self._window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def render_category_options(self) -> None:
        """Displays the data category options to choose from."""

        # checkbox values:
        ################################################################################################################
        self.category_to_value = {
            'passengers_can_us_int': tk.IntVar(),
            'passengers_can_not_us': tk.IntVar(),
            'freight_can_us_vehicles': tk.IntVar(),
            'freight_intl_teu': tk.IntVar(),
            'export_cash': tk.IntVar(),
            'import_cash': tk.IntVar(),
            'overall_air_passengers': tk.IntVar(),
            'overall_rail_passengers': tk.IntVar()
        }
        ################################################################################################################

        # checkbox objects:
        ################################################################################################################
        self.category_to_checkbox = {
            'passengers_can_us_int': tk.Checkbutton(self._frame_categories, text='American/Canadian/International \
passengers between USA/Canada.', variable=self.category_to_value['passengers_can_us_int']).pack(side=tk.TOP,
                                                                                                anchor=tk.W),

            'passengers_can_not_us': tk.Checkbutton(self._frame_categories, text='Canadian/International passengers \
between USA/Canada.', variable=self.category_to_value['passengers_can_not_us']).pack(side=tk.TOP, anchor=tk.W),

            'freight_can_us_vehicles': tk.Checkbutton(self._frame_categories, text='Freight vehicles between \
USA/Canada.', variable=self.category_to_value['freight_can_us_vehicles']).pack(side=tk.TOP, anchor=tk.W),

            'freight_intl_teu': tk.Checkbutton(self._frame_categories, text='International freight.',
                                               variable=self.category_to_value['freight_intl_teu']).pack(side=tk.TOP,
                                                                                                         anchor=tk.W),

            'export_cash': tk.Checkbutton(self._frame_categories, text='Value of export of goods.',
                                          variable=self.category_to_value['export_cash']).pack(side=tk.TOP,
                                                                                               anchor=tk.W),

            'import_cash': tk.Checkbutton(self._frame_categories, text='Value of import of goods.',
                                          variable=self.category_to_value['import_cash']).pack(side=tk.TOP,
                                                                                               anchor=tk.W),

            'overall_air_passengers': tk.Checkbutton(self._frame_categories, text='Air passengers.',
                                                     variable=self.category_to_value['overall_air_passengers'
                                                     ]).pack(side=tk.TOP, anchor=tk.W),

            'overall_rail_passengers': tk.Checkbutton(self._frame_categories, text='Rail passengers.',
                                                      variable=self.category_to_value['overall_rail_passengers'
                                                      ]).pack(side=tk.TOP, anchor=tk.W),

        }
        ################################################################################################################

    def render_filter_options(self) -> None:
        """Displays the data category options to filter."""
        # checkbox values:
        ################################################################################################################
        self.filter_to_value = {
            'passengers_can_us_int': tk.IntVar(),
            'passengers_can_not_us': tk.IntVar(),
            'freight_can_us_vehicles': tk.IntVar(),
            'freight_intl_teu': tk.IntVar(),
            'export_cash': tk.IntVar(),
            'import_cash': tk.IntVar(),
            'overall_air_passengers': tk.IntVar(),
            'overall_rail_passengers': tk.IntVar()
        }
        ################################################################################################################

        # checkbox objects:
        ################################################################################################################
        self.filter_to_checkbox = {
            'passengers_can_us_int': tk.Checkbutton(self._frame_filters, text='American/Canadian/International \
passengers between USA/Canada.', variable=self.filter_to_value['passengers_can_us_int']).pack(side=tk.TOP,
                                                                                              anchor=tk.W),

            'passengers_can_not_us': tk.Checkbutton(self._frame_filters, text='Canadian/International passengers \
between USA/Canada.', variable=self.filter_to_value['passengers_can_not_us']).pack(side=tk.TOP, anchor=tk.W),

            'freight_can_us_vehicles': tk.Checkbutton(self._frame_filters, text='Freight vehicles between \
USA/Canada.', variable=self.filter_to_value['freight_can_us_vehicles']).pack(side=tk.TOP, anchor=tk.W),

            'freight_intl_teu': tk.Checkbutton(self._frame_filters, text='International freight.',
                                               variable=self.filter_to_value['freight_intl_teu']).pack(
                side=tk.TOP,
                anchor=tk.W),

            'export_cash': tk.Checkbutton(self._frame_filters, text='Value of export of goods.',
                                          variable=self.filter_to_value['export_cash']).pack(side=tk.TOP,
                                                                                             anchor=tk.W),

            'import_cash': tk.Checkbutton(self._frame_filters, text='Value of import of goods.',
                                          variable=self.filter_to_value['import_cash']).pack(side=tk.TOP,
                                                                                             anchor=tk.W),

            'overall_air_passengers': tk.Checkbutton(self._frame_filters, text='Air passengers.',
                                                     variable=self.filter_to_value['overall_air_passengers'
                                                     ]).pack(side=tk.TOP, anchor=tk.W),

            'overall_rail_passengers': tk.Checkbutton(self._frame_filters, text='Rail passengers.',
                                                      variable=self.filter_to_value['overall_rail_passengers'
                                                      ]).pack(side=tk.TOP, anchor=tk.W),

        }
        ################################################################################################################

        # additional filter checkbox values
        ################################################################################################################
        self.additional_filter_to_value = {
            'filter_garbage': tk.IntVar(),
            'filter_duplicates': tk.IntVar()
        }
        ################################################################################################################

        # additional filter checkbox objects:
        ################################################################################################################
        self.additional_filter_to_checkbox = {
            'filter_garbage': tk.Checkbutton(self._frame_filters, text='Filter garbage data.',
                                             variable=self.additional_filter_to_value['filter_garbage'
                                             ]).pack(side=tk.TOP, anchor=tk.W),
            'filter_duplicates': tk.Checkbutton(self._frame_filters, text='Filter duplicate data.',
                                             variable=self.additional_filter_to_value['filter_duplicates'
                                             ]).pack(side=tk.TOP, anchor=tk.W)
        }

        # update button:
        ################################################################################################################
        self.update_graph_btn = tk.Button(self._frame_filters, text='Render Graph',
                                            command=self.update_graph).pack(side=tk.TOP, anchor=tk.E)
        ################################################################################################################

    def load_default_categories(self) -> None:
        """Reset categories_to_plot to plot all data categories."""
        self.categories_to_plot = [
            'passengers_can_us_int',
            'passengers_can_not_us',
            'freight_can_us_vehicles',
            'freight_intl_teu',
            'export_cash',
            'import_cash',
            'overall_air_passengers',
            'overall_rail_passengers'
        ]

    def update_graph(self) -> None:
        self.update_categories()
        self.update_additional_filters()
        filtered_data = self.update_filters()
        self.draw_graph(filtered_data)


    def update_categories(self) -> None:
        """Update categories_to_plot to plot the selected data categories."""
        self.categories_to_plot = [category for category in self.category_to_value if
                                   self.category_to_value[category].get() == 1]
        if not self.categories_to_plot:
            self.load_default_categories()

    def update_filters(self) -> list[OneMonthData]:
        self.categories_to_filter = [filter for filter in self.filter_to_value if
                                     self.filter_to_value[filter].get() == 1]
        return self.filter_values()

    def update_additional_filters(self) -> None:
        self.additional_filters = [self.additional_filter_to_value[additional_filter].get() == 1 for
                                   additional_filter in self.additional_filter_to_value]

    def filter_values(self) -> list[OneMonthData]:
        return filter(self.additional_filters[0], self.additional_filters[1], self.categories_to_filter, self.data)

    def draw_graph(self, custom_data: list[OneMonthData] = None) -> None:
        if custom_data:
            graphing.generate_graph(custom_data, self.categories_to_plot)
        else:
            graphing.generate_graph(self.data, self.categories_to_plot)

    def render_window(self) -> None:
        """Begin rendering the main window."""
        self._window.mainloop()


if __name__ == '__main__':
    project = CSProject('CSC110 Project: People, Cargo & CoVID', (450, 600))
    project.data = process_file(r'TestData.csv')
    project.render_window()
