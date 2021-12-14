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
import data_collection as dc
import data_filtering as df
import graphing


@dataclass
class CSProject:
    """Renders the main window for the Project."""
    data: list[dc.OneMonthData]
    categories_to_plot: list[str]
    categories_to_filter: list[str]
    _window: tk.Tk
    _frame_categories: tk.LabelFrame
    _frame_filters: tk.LabelFrame
    update_categories_btn: tk.Button
    update_filters_btn: tk.Button
    category_to_value: dict[str, tk.IntVar]
    category_to_checkbox: dict[str, tk.Checkbutton]
    filter_to_value: dict[str, tk.IntVar]
    filter_to_checkbox: dict[str, tk.Checkbutton]

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
        self._frame_categories.grid(row=0, column=0, padx=10)

        self._frame_filters = tk.LabelFrame(self._window, text='Filter Options', padx=5, pady=5)
        self._frame_filters.grid(row=1, column=0, padx=10)
        ################################################################################################################

        self.render_category_options()
        self.render_filter_options()

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
            'passengers_can_us_int': tk.Checkbutton(self._frame_categories, text='American/Canadian/International\
passengers between USA/Canada.', variable=self.category_to_value['passengers_can_us_int']).pack(side=tk.TOP,
                                                                                                anchor=tk.W),

            'passengers_can_not_us': tk.Checkbutton(self._frame_categories, text='Canadian/International passengers\
between USA/Canada.', variable=self.category_to_value['passengers_can_not_us']).pack(side=tk.TOP, anchor=tk.W),

            'freight_can_us_vehicles': tk.Checkbutton(self._frame_categories, text='Freight vehicles between\
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

        # update button:
        ################################################################################################################
        self.update_categories_btn = tk.Button(self._frame_categories, text='Update',
                                               command=self.update_categories).pack(side=tk.TOP, anchor=tk.E)
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
            'passengers_can_us_int': tk.Checkbutton(self._frame_filters, text='American/Canadian/International\
passengers between USA/Canada.', variable=self.filter_to_value['passengers_can_us_int']).pack(side=tk.TOP,
                                                                                              anchor=tk.W),

            'passengers_can_not_us': tk.Checkbutton(self._frame_filters, text='Canadian/International passengers\
between USA/Canada.', variable=self.filter_to_value['passengers_can_not_us']).pack(side=tk.TOP, anchor=tk.W),

            'freight_can_us_vehicles': tk.Checkbutton(self._frame_filters, text='Freight vehicles between\
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

        # update button:
        ################################################################################################################
        self.update_filters_btn = tk.Button(self._frame_filters, text='Update',
                                            command=self.update_filters).pack(side=tk.TOP, anchor=tk.E)
        ################################################################################################################

    def update_categories(self) -> None:
        self.categories_to_plot = [category for category in self.category_to_value if
                                   self.category_to_value[category].get() == 1]
        self.draw_graph()

    def update_filters(self) -> None:
        self.categories_to_filter = [filter for filter in self.filter_to_value if
                                     self.filter_to_value[filter].get() == 1]
        self.filter_values()
        self.draw_graph()

    def filter_values(self) -> None:
        self.data = df.filter(False, False, self.categories_to_filter, self.data)

    def draw_graph(self) -> None:
        graphing.generategraph(self.data, self.categories_to_plot)

    def render_window(self) -> None:
        """Begin rendering the main window."""
        self._window.mainloop()
        self.draw_graph()


if __name__ == '__main__':
    project = CSProject('CSC110 Project: People, Cargo & CoVID', (1280, 720))
    project.data = dc.process_file(r'TestData.csv')
    project.render_window()
