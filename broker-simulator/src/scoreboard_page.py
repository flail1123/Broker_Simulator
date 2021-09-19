import base_def
from tkinter import Frame, Canvas, LEFT, BOTH, ttk, RIGHT, Y, Label, StringVar, X, ttk, W, S, CENTER
from PIL import ImageTk, Image
from datetime import datetime
import os
import json

number_of_rows_to_display = 15


def format_date(records):
    for i, (date_string, budget, date_played_string) in enumerate(records):
        date = datetime.strptime(date_string, '%Y %m %d')
        date_played = datetime.strptime(date_played_string, '%Y-%m-%d_%H-%M-%S')
        records[i] = (date, budget, date_played)

    return records


def get_records():
    result = []
    for file in os.listdir('saves'):
        if file.startswith("score"):
            with open(os.path.join('saves', file)) as f:
                dictionary = json.load(f)
                result.append((dictionary['date'], int(dictionary['budget']), dictionary['date_played']))

    return format_date(result)


class ScoreboardPage:
    def create_back_button(self):
        # for back button in upper left corner
        back_button_x = int(base_def.pad_horizontal * self.screen_width)
        back_button_y = int(self.button_height)

        back_button = base_def.FramedButton(self.root, self.navigate.scoreboard_to_main, "Back to menu",
                                            self.metallic_yellow,  int(self.button_width / 2), self.button_height,
                                            self.font_style, self.font_color)
        return back_button, back_button_x, back_button_y

    def create_style_for_scoreboard(self, dark_mode):
        style = ttk.Style()
        style.theme_use("default")

        if not dark_mode:
            style.configure("Treeview", background="light grey", foreground="black",
                            rowheight=int(0.5 * self.screen_height) // number_of_rows_to_display,
                            fieldbackground="light grey")
        else:
            style.configure("Treeview", background="grey8", foreground="light grey",
                            rowheight=int(0.5 * self.screen_height) // number_of_rows_to_display,
                            fieldbackground="grey8")

        style.configure("Treeview.Heading", font=self.font_style,
                        height=int(0.5 * self.screen_height) // number_of_rows_to_display)
        style.map('Treeview', background=[('selected', 'invalid', 'green')],
                  foreground=[('selected', 'invalid', 'black')])
        return style

    def insert_records(self):
        for i, (date, budget, date_played) in enumerate(self.records):
            self.scoreboard.insert(parent='', index='end', iid=i, text="", values=(
            date.strftime("%Y-%m-%d"), budget, date_played.strftime("%Y-%m-%d %H:%M:%S")), tag='DEFAULT')

    def sort_scoreboard(self, event):
        region = self.scoreboard.identify('region', event.x, event.y)
        column = self.scoreboard.identify('column', event.x, event.y)
        if region == "heading":
            self.scoreboard.delete(*self.scoreboard.get_children())
            sorted_records = sorted(self.records, key=(lambda x: x[int(column[1]) - 1]))
            if sorted_records == self.records:
                self.records.reverse()
            else:
                self.records = sorted_records
            self.insert_records()

    def highlight_row(self, event):
        item = self.scoreboard.identify_row(event.y)
        self.scoreboard.tk.call(self.scoreboard, "tag", "remove", "highlight")
        self.scoreboard.tk.call(self.scoreboard, "tag", "add", "highlight", item)

    def create_scoreboard(self, dark_mode):
        scoreboard = ttk.Treeview(self.root, height=number_of_rows_to_display)
        scoreboard['columns'] = ("date", "budget", "date played")
        scoreboard.column("#0", width=0, minwidth=0)
        scoreboard.column("budget", anchor=CENTER, width=int(0.2 * self.screen_width),
                          minwidth=int(0.2 * self.screen_width))
        scoreboard.column("date", anchor=CENTER, width=int(0.15 * self.screen_width),
                          minwidth=int(0.15 * self.screen_width))
        scoreboard.column("date played", anchor=CENTER, width=int(0.25 * self.screen_width),
                          minwidth=int(0.25 * self.screen_width))

        scoreboard.heading("#0", anchor=CENTER, text="")
        scoreboard.heading("budget", anchor=CENTER, text="BUDGET")
        scoreboard.heading("date", anchor=CENTER, text="DATE")
        scoreboard.heading("date played", anchor=CENTER, text="LAST DATE PLAYED")
        scoreboard.bind("<ButtonRelease-1>", self.sort_scoreboard)
        scoreboard.bind("<Motion>", self.highlight_row)
        if not dark_mode:
            scoreboard.tag_configure('highlight', background='silver')
        else:
            scoreboard.tag_configure('highlight', background='black', foreground='white')
        return scoreboard

    def __init__(self, root, screen_info, navigation, dark_mode):
        self.on_display = False
        self.root = root
        self.screen_res, self.screen_width, self.screen_height, _, _, \
            self.background_photo_scoreboard_label, _, self.metallic_yellow, \
            self.base_beige, self.base_color, self.font_color = screen_info

        self.button_width, self.button_height, self.button_distance, self.button_border_width, self.font_style, \
            self.stock_list_width = base_def.create_settings(self.screen_res, self.screen_width, self.screen_height)
        self.navigate = navigation
        self.records = None
        self.style = self.create_style_for_scoreboard(dark_mode)
        self.scoreboard = self.create_scoreboard(dark_mode)
        self.back_button, self.back_button_x, self.back_button_y = self.create_back_button()

    def display(self):
        self.background_photo_scoreboard_label.place(x=0, y=0)
        self.scoreboard.tag_configure('DEFAULT', font=self.font_style)
        self.records = get_records()
        self.insert_records()
        self.scoreboard.place(x=int(0.2 * self.screen_width), y=int(0.3 * self.screen_height))
        self.back_button.get_frame().place(x=self.back_button_x, y=self.back_button_y)
        self.on_display = True

    def hide(self):
        self.back_button.get_frame().place_forget()
        self.scoreboard.delete(*self.scoreboard.get_children())
        self.scoreboard.place_forget()
        self.background_photo_scoreboard_label.place_forget()
        self.on_display = False
