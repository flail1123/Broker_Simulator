from datetime import *
from tkinter import *
import base_def
import textwrap


class EventsListbox:

    def __init__(self, root, events_data, button_border_width, font_style, stock_list_width, base_color):
        self.root = root
        self.stock_list_width = stock_list_width
        self.events_data = events_data
        self.frame = base_def.Frame(self.root, highlightbackground="black",
                                    highlightthickness=button_border_width, bd=0)
        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.list = Listbox(self.frame, bg=base_color, bd=0, font=font_style, fg='black',
                            height=10, width=stock_list_width, selectforeground='black',
                            selectmode=NONE, activestyle="none", selectbackground=base_color,
                            yscrollcommand=scrollbar.set, highlightthickness=0)
        scrollbar.config(command=self.list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.pack()
        self.displayed_events = []

    def update(self, new_events):
        n = 25
        for ev in new_events:
            self.displayed_events.append(ev)
            d, evdsc = ev.split(' ', 1)
            chunks = textwrap.wrap(evdsc, self.stock_list_width, break_long_words=False)
            self.list.insert(0, " ")
            i = len(chunks) - 1
            while i >= 0:
                self.list.insert(0, chunks[i])
                i -= 1
            self.list.insert(0, d)

    def clear(self):
        self.list.delete(0, END)
