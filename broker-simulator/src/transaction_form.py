from tkinter import *
from PIL import ImageTk, Image
import base_def
import math


class TransactionForm:

    def create_buttons(self):
        buy_button = base_def.FramedButton(self.root, self.buy_stock, "Buy", self.metallic_yellow,
                                           self.button_width // 2, self.button_height, self.font_style,
                                           self.font_color, True)

        sell_button = base_def.FramedButton(self.root, self.sell_stock, "Sell", self.metallic_yellow,
                                            self.button_width // 2, self.button_height, self.font_style,
                                            self.font_color, True)
        search_button = base_def.FramedButton(self.root, self.filter_companies_listbox, "", self.search_icon,
                                              self.input_txt.winfo_reqheight(), self.input_txt.winfo_reqheight(),
                                              self.font_style, self.font_color)
        return buy_button, sell_button, search_button

    def create_labels(self):
        amount_to_pay = DoubleVar()
        amount_to_pay.set(0)
        amount_to_pay_label = base_def.FramedLabel(self.root, amount_to_pay, self.metallic_yellow,
                                                   self.button_width // 2, self.button_height,
                                                   self.font_style, self.font_color)
        amount_to_pay_label.get_label().config(fg=self.font_color)
        amount_to_receive = DoubleVar()
        amount_to_receive.set(0)
        amount_to_receive_label = base_def.FramedLabel(self.root, amount_to_receive, self.metallic_yellow,
                                                       self.button_width // 2, self.button_height,
                                                       self.font_style, self.font_color)
        amount_to_receive_label.get_label().config(fg=self.font_color)
        budget = StringVar()
        budget.set(str(self.stocks_portfolio.get_budget()) + "$")
        budget_label = base_def.FramedLabel(self.root, budget, self.metallic_yellow,
                                            self.button_width, self.button_height,
                                            self.font_style, self.font_color)
        budget_label.get_label().config(fg=self.font_color)
        notice = StringVar()
        notice_label = base_def.FramedLabel(self.root, notice, self.metallic_yellow,
                                            self.button_width // 2, self.button_height,
                                            self.font_style, self.font_color)

        return amount_to_pay_label, amount_to_pay, amount_to_receive_label, amount_to_receive, budget_label, budget, notice_label, notice

    def create_listboxes(self):
        companies_listbox_frame = base_def.Frame(self.root, highlightbackground="black",
                                                 highlightthickness=self.button_border_width, bd=0)
        scrollbar = Scrollbar(companies_listbox_frame, orient=VERTICAL)
        scrollbar2 = Scrollbar(companies_listbox_frame, orient=HORIZONTAL)
        companies_listbox = Listbox(companies_listbox_frame, bg=self.base_color, bd=0, font=self.font_style,
                                    fg='black', height=self.stocks_display, width=self.stock_list_width,
                                    selectmode=SINGLE, activestyle="none", selectbackground='black',
                                    yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set, highlightthickness=0,
                                    exportselection=0)
        companies_listbox.bind("<<ListboxSelect>>", self.companies_listbox_selected_stock)
        scrollbar.config(command=companies_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar2.config(command=companies_listbox.xview)
        scrollbar2.pack(fill=X)
        companies_listbox.pack()

        my_stock_listbox_frame = base_def.Frame(self.root, highlightbackground="black",
                                                highlightthickness=self.button_border_width, bd=0)
        scrollbar3 = Scrollbar(my_stock_listbox_frame, orient=VERTICAL)
        scrollbar4 = Scrollbar(companies_listbox_frame, orient=HORIZONTAL)
        my_stock_listbox = Listbox(my_stock_listbox_frame, bg=self.base_color, bd=0, font=self.font_style,
                                   fg='black', height=self.stocks_display, width=self.stock_list_width,
                                   selectmode=SINGLE, activestyle="none", selectbackground='black',
                                   yscrollcommand=scrollbar3.set, xscrollcommand=scrollbar4.set, highlightthickness=0,
                                   exportselection=0)
        my_stock_listbox.bind("<<ListboxSelect>>", self.my_stock_listbox_selected_stock)
        scrollbar3.config(command=my_stock_listbox.yview)
        scrollbar3.pack(side=RIGHT, fill=Y)
        scrollbar4.config(command=companies_listbox.xview)
        scrollbar4.pack(fill=X)
        my_stock_listbox.pack()

        return companies_listbox, companies_listbox_frame, my_stock_listbox, my_stock_listbox_frame

    def create_scales(self):
        buy_scale = Scale(from_=0, to=50, orient=HORIZONTAL, command=self.choose_amount_to_buy, bg=self.base_color,
                          label="Amount:", font=self.font_style, troughcolor="black", length=200)
        sell_scale = Scale(from_=0, to=50, orient=HORIZONTAL, command=self.choose_amount_to_sell, bg=self.base_color,
                           label="Amount:", font=self.font_style, troughcolor="black", length=200)
        return buy_scale, sell_scale

    def __init__(self, root, screen_info, navigation, stocks_data, stocks_portfolio):
        self.on_display = False
        self.stocks_portfolio = stocks_portfolio
        self.current_date = None
        # initiate base settings
        self.screen_res, self.screen_width, self.screen_height, _, self.background_photo_label, _, _, \
            self.metallic_yellow, self.base_beige, self.base_color, self.font_color = screen_info
        self.root = root
        self.navigate = navigation
        self.stocks_data = stocks_data
        self.button_width, self.button_height, self.button_distance, \
            self.button_border_width, self.font_style, self.stock_list_width = \
            base_def.create_settings(self.screen_res, self.screen_width, self.screen_height)

        self.stocks_display = int(self.button_height / 2)

        self.companies_listbox, self.companies_listbox_frame, self.my_stock_listbox, self.my_stock_listbox_frame = \
            self.create_listboxes()

        self.list_placement_x = int(base_def.pad_horizontal * self.screen_width)
        self.list_placement_y = int(base_def.pad_vertical * self.screen_height)

        self.input_txt = Text(root, height=1,
                              width=self.stock_list_width - self.stocks_display // 10,
                              bg="white")
        search_icon = Image.open('images/search.png')
        self.search_icon = ImageTk.PhotoImage(
            search_icon.resize((self.input_txt.winfo_reqheight(), self.input_txt.winfo_reqheight()),
                               Image.ANTIALIAS))
        self.back_to_sim_btn = base_def.FramedButton(self.root, self.navigate.transaction_to_simulation, "Back",
                                                     self.metallic_yellow, int(self.button_width / 2), self.button_height,
                                                     self.font_style, self.font_color)


        self.buy_scale, self.sell_scale = self.create_scales()
        self.amount_to_pay_label, self.amount_to_pay, self.amount_to_receive_label, self.amount_to_receive, \
            self.budget_label, self.budget, self.notice_label, self.notice = self.create_labels()

        self.dictionary_of_abbreviations = self.stocks_data.abbreviations
        self.stock_list = None

        self.back_btn_x = int(base_def.pad_horizontal * self.screen_width)
        self.back_btn_y = int(self.button_height)
        self.buy_button, self.sell_button, self.search_button = self.create_buttons()

    def companies_listbox_selected_stock(self, event):
        self.buy_scale.set(0)
        selected_stock_line = self.companies_listbox.get(self.companies_listbox.curselection()[0])
        selected_stock = selected_stock_line[:selected_stock_line.find(':')]
        price = self.stocks_data.get_price(selected_stock, self.current_date)
        budget = self.stocks_portfolio.get_budget()
        scale_range = math.floor(budget / price)
        self.buy_scale.config(to=scale_range)

    def my_stock_listbox_selected_stock(self, event):
        self.sell_scale.set(0)
        if len(self.my_stock_listbox.curselection()) > 0:
            selected_stock_line = self.my_stock_listbox.get(self.my_stock_listbox.curselection()[0])
        else:
            selected_stock_line = self.my_stock_listbox.get(0)
        selected_stock = selected_stock_line[:selected_stock_line.find(':')]
        scale_range = self.stocks_portfolio.how_many_stocks(selected_stock)
        self.sell_scale.config(to=scale_range)

    def update_my_stock_listbox(self, stock):
        amount = self.stocks_portfolio.how_many_stocks(stock)
        list_of_lines = self.my_stock_listbox.get(0, END)
        for i, line in enumerate(list_of_lines):
            if stock in line:
                self.my_stock_listbox.delete(i)
                if amount != 0:
                    line = stock + ": " + self.dictionary_of_abbreviations[stock] + " (" + str(amount) + ")"
                    self.my_stock_listbox.insert(i, line)
                    if len(self.my_stock_listbox.curselection()) == 0:
                        self.my_stock_listbox.selection_set(i)
                        self.my_stock_listbox_selected_stock(None)
                elif self.my_stock_listbox.size() != 0 and len(self.my_stock_listbox.curselection()) == 0:
                    self.my_stock_listbox.selection_set(0)
                    self.my_stock_listbox_selected_stock(None)
                return
        line = stock + ": " + self.dictionary_of_abbreviations[stock] + " (" + str(amount) + ")"
        self.my_stock_listbox.insert(END, line)
        if self.my_stock_listbox.size() == 1:
            self.my_stock_listbox.selection_set(self.my_stock_listbox.size() - 1)
            self.my_stock_listbox_selected_stock(None)

    def sell_stock(self):
        try:
            if len(self.my_stock_listbox.curselection()) != 0:
                selected_stock_line = self.my_stock_listbox.get(self.my_stock_listbox.curselection()[0])
                selected_stock = selected_stock_line[:selected_stock_line.find(':')]
                amount = self.sell_scale.get()
                if amount != 0:
                    self.stocks_portfolio.sell_stocks(selected_stock, amount, self.current_date)
                    self.update_my_stock_listbox(selected_stock)
                    self.budget.set(str(self.stocks_portfolio.get_budget()) + "$")
                    self.notice_label.get_frame().grid_forget()
                    self.companies_listbox_selected_stock(None)
        except:
            self.notice.set("Not enough stock!")
            self.notice_label.get_frame().grid(row=2, column=4, pady=(self.button_height * 6, 0))

    def buy_stock(self):
        try:
            if len(self.companies_listbox.curselection()) != 0:
                selected_stock_line = self.companies_listbox.get(self.companies_listbox.curselection()[0])
                selected_stock = selected_stock_line[:selected_stock_line.find(':')]
                amount = self.buy_scale.get()
                if amount != 0:
                    self.stocks_portfolio.buy_stocks(selected_stock, amount, self.current_date)
                    self.update_my_stock_listbox(selected_stock)
                    self.budget.set(str(self.stocks_portfolio.get_budget()) + "$")
                    self.notice_label.get_frame().grid_forget()
                    self.companies_listbox_selected_stock(None)
        except:
            self.notice.set("Not enough money!")
            self.notice_label.get_frame().grid(row=2, column=2, pady=(self.button_height * 6, 0))

    def choose_amount_to_buy(self, amount):
        if len(self.companies_listbox.curselection()) != 0:
            selected_stock_line = self.companies_listbox.get(self.companies_listbox.curselection()[0])
            selected_stock = selected_stock_line[:selected_stock_line.find(':')]
            selected_stock_price = self.stocks_data.get_price(selected_stock, self.current_date)
            self.amount_to_pay.set(round(int(amount) * selected_stock_price, 2))

    def choose_amount_to_sell(self, amount):
        if len(self.my_stock_listbox.curselection()) != 0:
            selected_stock_line = self.my_stock_listbox.get(self.my_stock_listbox.curselection()[0])
            selected_stock = selected_stock_line[:selected_stock_line.find(':')]
            selected_stock_price = self.stocks_data.get_price(selected_stock, self.current_date)
            self.amount_to_receive.set(round(int(amount) * selected_stock_price, 2))

    def display(self, current_date):
        self.current_date = current_date
        self.stock_list = self.stocks_data.get_stocks_name_and_price_in_date(current_date)

        self.budget_label.get_frame().grid(row=1, column=2, pady=(self.button_height, 0))

        # column 1
        self.background_photo_label.place(x=0, y=0)
        self.companies_listbox_frame.grid(row=2, column=1, padx=(self.list_placement_x, 0),
                                          pady=(self.list_placement_y, 0))
        self.fill_companies_listbox()
        self.search_button.get_frame().grid(row=3, column=1,
                                            padx=(self.list_placement_x + self.input_txt.winfo_reqwidth(), 0),
                                            pady=(10, 0))
        self.input_txt.grid(row=3, column=1, padx=(self.list_placement_x / 2, 0), pady=(10, 0))

        # column 2
        self.buy_scale.grid(row=2, column=2, pady=(0, self.button_height * 4))
        self.amount_to_pay_label.get_frame().grid(row=2, column=2)
        self.buy_button.get_frame().grid(row=2, column=2, pady=(self.button_height * 3, 0))

        # column 3
        self.my_stock_listbox_frame.grid(row=2, column=3, padx=(self.list_placement_x, self.button_width // 4),
                                         pady=(self.list_placement_y, 0))
        self.fill_my_stock_listbox()
        # column 4
        self.sell_scale.grid(row=2, column=4, pady=(0, self.button_height * 4))
        self.amount_to_receive_label.get_frame().grid(row=2, column=4)
        self.sell_button.get_frame().grid(row=2, column=4, pady=(self.button_height * 3, 0))

        self.back_to_sim_btn.get_frame().place(x=self.back_btn_x, y=self.back_btn_y)

        self.on_display = True

    def hide(self):
        self.buy_scale.grid_forget()
        self.sell_scale.grid_forget()
        self.input_txt.grid_forget()
        self.search_button.get_frame().grid_forget()
        self.companies_listbox_frame.grid_forget()
        self.background_photo_label.place_forget()
        self.amount_to_pay_label.get_frame().grid_forget()
        self.buy_button.get_frame().grid_forget()
        self.sell_button.get_frame().grid_forget()
        self.budget_label.get_frame().grid_forget()
        self.my_stock_listbox_frame.grid_forget()
        self.amount_to_receive_label.get_frame().grid_forget()
        self.notice_label.get_frame().grid_forget()
        self.my_stock_listbox.delete(0, END)
        self.companies_listbox.delete(0, END)
        self.back_to_sim_btn.get_frame().place_forget()
        self.on_display = False

    def fill_my_stock_listbox(self):
        for stock, _ in self.stock_list:
            amount = self.stocks_portfolio.how_many_stocks(stock)
            if self.stocks_portfolio.how_many_stocks(stock) != 0:
                self.my_stock_listbox.insert(END, stock + ": " + self.dictionary_of_abbreviations[stock] + " (" + str(
                    amount) + ")")
        if self.my_stock_listbox.size() != 0:
            self.my_stock_listbox.selection_set(0)
            self.my_stock_listbox_selected_stock(None)

    def fill_companies_listbox(self):
        for stock, price in self.stock_list:
            if stock in self.dictionary_of_abbreviations.keys():
                self.companies_listbox.insert(END, stock + ": " + self.dictionary_of_abbreviations[stock] + " (" + str(
                    price) + "$)")
        if self.companies_listbox.size() != 0:
            self.companies_listbox.selection_set(0)
            self.companies_listbox_selected_stock(None)

    def filter_companies_listbox(self):
        searched = self.input_txt.get("1.0", "end-1c")
        if searched == "":
            self.fill_companies_listbox()
        else:
            self.companies_listbox.delete(0, END)
            for stock, price in self.stock_list:
                if stock in self.dictionary_of_abbreviations.keys():
                    name = self.dictionary_of_abbreviations[stock]
                    if searched.lower() in name.lower():
                        self.companies_listbox.insert(END, stock + ": " + name + " (" + str(price) + "$)")
        if self.companies_listbox.size() != 0:
            self.companies_listbox.selection_set(0)
            self.companies_listbox_selected_stock(None)
