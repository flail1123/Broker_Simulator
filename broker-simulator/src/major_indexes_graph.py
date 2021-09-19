import base_def
from plots import fig_init, axis_color, axis_color_dark
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import *
import matplotlib.pyplot as plt
from tkcalendar import *
from tkinter import StringVar


class MajorIndexesGraph:
    def create_graph(self):
        fig, ax = fig_init(self.statistics_page.screen_width, self.statistics_page.dark_mode)
        canvas = FigureCanvasTkAgg(fig, self.statistics_page.root)
        self.statistics_page.stocks_data.load_indexes()
        return canvas, ax, fig

    def update_graph(self, index):
        self.index = index
        self.ax.clear()
        self.ax.set(xlabel='Date', ylabel='Index Value')
        if not self.statistics_page.dark_mode:
            self.ax.set_facecolor(axis_color)
        else:
            self.ax.set_facecolor(axis_color_dark)
        self.ax.grid()

        data = self.statistics_page.stocks_data.get_indexes(self.date_from, self.date_to, index)

        self.ax.plot([i[0] for i in data], [i[1] for i in data], label=self.dictionary[index])

        self.ax.legend(framealpha=1.0, loc='upper left')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def create_indexes_buttons(self):
        indexes_buttons = []
        functions = [lambda: self.update_graph('djia'), lambda: self.update_graph('nasdaqc'),
                     lambda: self.update_graph('s_and_p500'), lambda: self.update_graph('vix')]
        for i, (key, value) in enumerate(self.dictionary.items()):
            indexes_buttons.append(base_def.FramedButton(self.statistics_page.root, functions[i], value,
                                                         self.statistics_page.metallic_yellow,
                                                         self.statistics_page.button_width // 1.3,
                                                         self.statistics_page.button_height,
                                                         self.statistics_page.font_style,
                                                         self.statistics_page.font_color))
        return indexes_buttons

    def next_graph(self):
        self.hide()
        self.statistics_page.current_graph = 2
        self.statistics_page.graph_2.display()

    def create_next_graph_button(self):
        return base_def.FramedButton(self.statistics_page.root, self.next_graph, "Next Graph",
                              self.statistics_page.metallic_yellow,
                              self.statistics_page.button_width // 1.3,
                              self.statistics_page.button_height,
                              self.statistics_page.font_style,
                              self.statistics_page.font_color)


    def submit_date(self):
        self.date_from = self.date_from_calendar.selection_get()

        self.date_to = self.date_to_calendar.selection_get()

        self.update_graph(self.index)

    def create_calendars(self):
        calendar_from = Calendar(self.statistics_page.root, selectmode="day", year=2014, month=5, day=22)
        calendar_to = Calendar(self.statistics_page.root, selectmode="day", year=2015, month=5, day=22)
        submit_date_button = base_def.FramedButton(self.statistics_page.root, self.submit_date, "Submit",
                                                   self.statistics_page.metallic_yellow,
                                                   self.statistics_page.button_width // 2.1,
                                                   self.statistics_page.button_height, self.statistics_page.font_style,
                                                   self.statistics_page.font_color)
        end_date = StringVar()
        end_date.set("End date")
        date_to_label = base_def.FramedLabel(self.statistics_page.root, end_date, self.statistics_page.metallic_yellow,
                                             self.statistics_page.button_width // 2,
                                             self.statistics_page.button_height // 1.5, self.statistics_page.font_style,
                                             self.statistics_page.font_color)
        start_date = StringVar()
        start_date.set("Start date")
        date_from_label = base_def.FramedLabel(self.statistics_page.root, start_date,
                                               self.statistics_page.metallic_yellow,
                                               self.statistics_page.button_width // 2,
                                               self.statistics_page.button_height // 1.5,
                                               self.statistics_page.font_style,
                                               self.statistics_page.font_color)

        return calendar_from, calendar_to, submit_date_button, date_to_label, date_from_label

    def __init__(self, statistics_page):
        self.statistics_page = statistics_page
        self.on_display = False

        self.date_from = date(2014, 5, 22)
        self.date_to = date(2015, 5, 22)

        self.date_from_calendar, self.date_to_calendar, self.submit_date_button, \
        self.date_to_label, self.date_from_label = self.create_calendars()

        self.dictionary = {'djia': "Dow Jones Industrial Average", 'nasdaqc': "NASDAQ Composite Index", 's_and_p500':
            "S&P500", 'vix': "Cboe Volatility Index"}

        self.index = 's_and_p500'

        self.indexes_buttons = self.create_indexes_buttons()
        self.next_graph_button = self.create_next_graph_button()

        self.canvas, self.ax, self.fig = self.create_graph()
        self.update_graph('vix')

    def display(self):
        self.on_display = True
        self.canvas.get_tk_widget().place(x=self.statistics_page.screen_width * 0.25,
                                          y=self.statistics_page.screen_height * 0.3)
        for i, button in enumerate(self.indexes_buttons):
            button.get_frame().place(x=self.statistics_page.screen_width * 0.07, y=self.statistics_page.screen_height *
                                0.3 + i * self.statistics_page.button_height * 3 + self.statistics_page.button_height)
        self.date_from_label.get_frame().place(x=self.statistics_page.screen_width * 0.815,
                                               y=self.statistics_page.screen_height * 0.3)
        self.date_from_calendar.place(x=self.statistics_page.screen_width * 0.8,
                                      y=self.statistics_page.screen_height * 0.335)
        self.date_to_label.get_frame().place(x=self.statistics_page.screen_width * 0.815,
                                             y=self.statistics_page.screen_height * 0.55)
        self.date_to_calendar.place(x=self.statistics_page.screen_width * 0.8,
                                    y=self.statistics_page.screen_height * 0.585)
        self.submit_date_button.get_frame().place(x=self.statistics_page.screen_width * 0.815,
                                                  y=self.statistics_page.screen_height * 0.8)
        self.next_graph_button.get_frame().place(x=self.statistics_page.screen_width * 0.815,
                                                  y=self.statistics_page.screen_height * 0.9)

    def hide(self):
        self.canvas.get_tk_widget().place_forget()
        for button in self.indexes_buttons:
            button.get_frame().place_forget()
        self.on_display = False
        self.date_from_label.get_frame().place_forget()
        self.date_from_calendar.place_forget()
        self.date_to_label.get_frame().place_forget()
        self.date_to_calendar.place_forget()
        self.submit_date_button.get_frame().place_forget()
        self.next_graph_button.get_frame().place_forget()
