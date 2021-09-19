from datetime import *
from tkinter import *
import base_def


class StockListbox:

    def __init__(self, root, stocks_data, button_border_width, font_style, stocks_display, stock_list_width, base_color):
        self.root = root
        self.stocks_data = stocks_data
        self.frame = base_def.Frame(self.root, highlightbackground="black",
                                    highlightthickness=button_border_width, bd=0)
        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        scrollbar2 = Scrollbar(self.frame, orient=HORIZONTAL)
        self.listbox = Listbox(self.frame, bg=base_color, bd=0, font=font_style, fg='black',
                               height=stocks_display, width=stock_list_width,
                               selectmode=MULTIPLE, activestyle="none", selectbackground='black',
                               yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set,
                               highlightthickness=0)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar2.config(command=self.listbox.xview)
        scrollbar2.pack(fill=X)
        self.listbox.pack()

        self.available_stock = []

    def prioritize_selected_stock(self):
        selected = self.selected_stock()
        for stock in selected:
            self.delete_stock_from_list(stock)
            self.add_stock_to_list(stock, where=0)
            self.listbox.selection_set(0)

    def update(self, new_stock, lost_stock):
        for stock in new_stock:
            self.add_stock_to_list(stock)
        for stock in lost_stock:
            self.delete_stock_from_list(stock)

    def delete_stock_from_list(self, stock_abbreviation):
        index_of_stock = self.available_stock.index(stock_abbreviation)
        self.listbox.delete(index_of_stock)
        self.available_stock.pop(index_of_stock)

    def add_stock_to_list(self, stock_abbreviation, where=END):
        if not self.stocks_data.is_abbreviation_correct(stock_abbreviation):
            return  # Not all abbreviations are in database
        if where == END:
            self.available_stock.append(stock_abbreviation)
        else:
            self.available_stock.insert(where, stock_abbreviation)
        stock_name = self.stocks_data.get_name_for_abbreviation(stock_abbreviation)
        self.listbox.insert(where, stock_name)

    def selected_stock(self):
        selected_stock_indexes = self.listbox.curselection()
        selected_stock = [self.available_stock[i] for i in selected_stock_indexes]
        return selected_stock
