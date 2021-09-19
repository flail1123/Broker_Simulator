import base_def
from datetime import *
from stock_listbox import StockListbox
from events_listbox import EventsListbox
from tkinter import *
import plots
from tkinter import ttk
import matplotlib.pyplot as plt

default_timeframe_days = 60
default_interval = 500
default_time_speed = 1


class SimulationPage:

    def __init__(self, root, screen_info, navigation, stocks_data, events_data, dark_mode, starting_date=None):
        self.on_display = False
        self.paused = True
        self.screen_res, self.screen_width, self.screen_height, _, self.background_photo_label, _, _,\
            self.metallic_yellow, self.base_beige, self.base_color, self.font_color = screen_info
        self.root = root
        self.navigate = navigation

        self.button_width, self.button_height, self.button_distance, \
            self.button_border_width, self.font_style, self.stock_list_width = \
            base_def.create_settings(self.screen_res, self.screen_width, self.screen_height)
        self.stocks_display = int(self.button_height / 2)
        self.list_placement_x = int(base_def.pad_horizontal * self.screen_width)
        self.list_placement_y = int(base_def.pad_vertical * self.screen_height)

        self.stock_listbox = StockListbox(root, stocks_data, self.button_border_width, self.font_style,
                                          self.stocks_display, self.stock_list_width, self.base_color)
        self.event_listbox = EventsListbox(root, events_data, self.button_border_width, self.font_style,
                                           self.stock_list_width, self.base_color)

        if not starting_date:
            self.current_date = base_def.min_date
        else:
            self.current_date = starting_date

        self.time_speed = default_time_speed

        self.days_to_display_filter, self.number_of_days_to_display, self.scale_graph_from_zero = self.create_graph_filters()

        self.change_time_speed_button, self.pause_unpause_button = self.create_time_manipulation_buttons()
        self.prioritize_selected_stock_button = base_def.FramedButton(self.root, self.stock_listbox.prioritize_selected_stock,
                                                                      "Prioritize Selected", self.metallic_yellow,
                                                                      self.stock_listbox.listbox.winfo_reqwidth(), self.button_height,
                                                                      self.font_style, self.font_color)

        self.base_interval = default_interval
        self.date_string = StringVar()
        self.date_label_framed = self.create_date_label_framed()
        self.graph_animation, self.graph_canvas = plots.draw_graph(self.root, stocks_data, events_data,
                                                                   self.stock_listbox, self.event_listbox,
                                                                   self.current_date, self.number_of_days_to_display,
                                                                   self.base_interval, self.date_string,
                                                                   self.scale_graph_from_zero,
                                                                   self.screen_width, dark_mode)
        self.back_btn, self.to_form_btn, self.back_btn_x, self.back_btn_y = \
            self.create_transition_buttons()
        self.save_game_btn, self.finish_game_btn = self.create_end_game_buttons()

    def stop_animation(self):
        self.graph_animation.event_source.stop()

    def create_time_manipulation_buttons(self):
        change_time_speed_button = base_def.FramedButton(self.root, self.change_time_speed,
                                                         "Time: >", self.metallic_yellow,
                                                         self.button_width // 2,
                                                         self.button_height, self.font_style, self.font_color)

        pause_unpause_button = base_def.FramedButton(self.root, self.pause_unpause,
                                                     "||", self.metallic_yellow,
                                                     self.button_width // 9,
                                                     self.button_height, self.font_style, self.font_color)

        return change_time_speed_button, pause_unpause_button

    def create_date_label_framed(self):
        date_label_frame = Frame(self.root, highlightbackground="black", highlightthickness=3, bd=0)

        date_label = Label(date_label_frame, font=self.font_style, textvariable=self.date_string,
                           image=self.metallic_yellow, height=self.button_height, width=self.button_width,
                           compound=CENTER, fg=self.font_color)
        date_label.pack()
        return date_label_frame

    def create_graph_filters(self):
        number_of_days_to_display = IntVar()
        number_of_days_to_display.set(default_timeframe_days)
        days_to_display_options = [10, 20, 30, 40, 60, 80, 100, 150]
        graph_filters = Frame(self.root, highlightbackground="black", highlightthickness=3, bd=0,
                              height=self.button_height, width=self.button_width * 5, bg=self.base_color)
        options_buttons = []
        days_to_display_label = Label(graph_filters, text="Days to display in graph: ", font=self.font_style,
                                      bg=self.base_color)
        days_to_display_label.grid(row=0, column=0)
        for i, option in enumerate(days_to_display_options):
            options_buttons.append(
                Radiobutton(graph_filters, text=str(option), variable=number_of_days_to_display, value=option,
                            font=self.font_style, bg=self.base_color))
            options_buttons[-1].grid(row=0, column=i + 1)
        change_graph_scale_label = Label(graph_filters, text="Scale: ", font=self.font_style, bg=self.base_color)
        change_graph_scale_label.grid(row=1, column=0)
        scale_graph_from_zero = BooleanVar()
        scale_graph_from_zero.set(False)
        relative_option = Radiobutton(graph_filters, text="relative", variable=scale_graph_from_zero, value=False,
                                      font=self.font_style, bg=self.base_color)
        relative_option.grid(row=1, column=1, columnspan=2)
        from_zero_option = Radiobutton(graph_filters, text="from zero", variable=scale_graph_from_zero, value=True,
                                       font=self.font_style, bg=self.base_color)
        from_zero_option.grid(row=1, column=3, columnspan=2)
        return graph_filters, number_of_days_to_display, scale_graph_from_zero

    def create_transition_buttons(self):
        # for back button in upper left corner
        back_btn_x = int(base_def.pad_horizontal * self.screen_width)
        back_btn_y = int(self.button_height)

        back_btn = base_def.FramedButton(self.root, self.navigate.simulation_to_main, "Back to menu", self.metallic_yellow,
                                         int(self.button_width / 2), self.button_height, self.font_style, self.font_color)
        to_form_btn = base_def.FramedButton(self.root, self.navigate.simulation_to_transaction, "Buy / Sell",
                                            self.metallic_yellow, int(self.button_width / 2), self.button_height,
                                            self.font_style, self.font_color)
        return back_btn, to_form_btn, back_btn_x, back_btn_y

    def create_end_game_buttons(self):
        save_game_btn = base_def.FramedButton(self.root, self.navigate.save_simulation,
                                              "Save game state", self.metallic_yellow,
                                              self.button_width, self.button_height, self.font_style, self.font_color).get_frame()
        finish_game_btn = base_def.FramedButton(self.root, self.navigate.finish_game,
                                                "Finish game", self.metallic_yellow,
                                                self.button_width, self.button_height, self.font_style, self.font_color).get_frame()
        return save_game_btn, finish_game_btn

    def display(self):
        self.background_photo_label.place(x=0, y=0)
        self.stock_listbox.frame.grid(row=2, column=0, padx=(self.list_placement_x, 0))
        self.event_listbox.frame.grid(row=2, column=3, padx=(0, self.list_placement_x), pady=(0, self.button_height * 5))
        self.graph_canvas.get_tk_widget().grid(row=2, column=1, padx=(self.list_placement_x, 0),
                                               pady=(self.list_placement_y - self.button_height * 2, 0))

        self.change_time_speed_button.get_frame().grid(row=0, column=3, pady=(self.button_height, 0), padx=(0, self.button_height))
        self.pause_unpause_button.get_frame().grid(row=0, column=2, pady=(self.button_height, 0), padx=(0, 10))

        self.date_label_framed.grid(row=0, column=1, pady=(self.button_height, 0))
        self.days_to_display_filter.grid(row=3, column=1, pady=(self.button_height, 0))
        self.prioritize_selected_stock_button.get_frame().grid(row=1, column=0, pady=(self.button_height, 10), padx=(self.list_placement_x, 0))
        self.on_display = True
        self.pause_unpause()
        # Added
        self.back_btn.get_frame().place(x=self.back_btn_x, y=self.back_btn_y)
        self.to_form_btn.get_frame().grid(column=3, row=3, pady=(self.button_height, 0), padx=(0, self.button_height))
        self.save_game_btn.grid(column=3, row=2, pady=(self.button_height * 4, 0), padx=(0, self.button_height))
        self.finish_game_btn.grid(column=3, row=2, pady=(self.button_height * 7, 0), padx=(0, self.button_height))

    def hide(self):
        # Added
        self.back_btn.get_frame().place_forget()
        self.to_form_btn.get_frame().grid_forget()
        self.save_game_btn.grid_forget()
        self.finish_game_btn.grid_forget()

        self.graph_canvas.get_tk_widget().grid_forget()
        self.event_listbox.frame.grid_forget()
        self.stock_listbox.frame.grid_forget()
        self.stock_listbox.listbox.selection_clear(0, END)
        self.background_photo_label.place_forget()
        self.change_time_speed_button.get_frame().grid_forget()
        self.pause_unpause_button.get_frame().grid_forget()
        self.date_label_framed.grid_forget()
        self.days_to_display_filter.grid_forget()
        self.prioritize_selected_stock_button.get_frame().grid_forget()
        self.on_display = False

    def change_time_speed(self):
        self.time_speed = ((self.time_speed - 1) + 1) % 4 + 1
        text = "Time: " + self.time_speed * '>'
        self.change_time_speed_button.get_button().config(text=text)
        self.graph_animation.event_source.interval = self.base_interval // self.time_speed

    def change_date(self, new_date):
        self.current_date = new_date

    def pause_unpause(self):
        if not self.paused:
            self.paused = True
            self.graph_animation.event_source.stop()
            text = ">"
        else:
            self.paused = False
            self.graph_animation.event_source.start()
            text = "||"
        self.pause_unpause_button.get_button().config(text=text)

    def get_paused(self):
        return self.paused
