from json import dump, load
from collections import defaultdict
from stocks_data import StocksData
from datetime import datetime

class TransactionError(Exception):
    """Raised when transaction was invalid for any reason"""


class StocksPortfolio:

    def __init__(self, stocks_data, starting_budget):
        self.stocks_data = stocks_data
        self.budget = starting_budget
        self.stocks_owned = defaultdict(lambda: 0)

    def buy_stocks(self, stock_name, quantity, date):
        price = float(self.stocks_data.get_price(stock_name, date))
        if price * quantity > self.budget:
            raise TransactionError  # Not enough funds to perform this operation
        self.budget = (int((self.budget - price * quantity) * 100))/100
        self.stocks_owned[stock_name] += quantity

    def sell_stocks(self, stock_name, quantity, date):
        if quantity > self.stocks_owned[stock_name]:
            raise TransactionError  # Not enough stocks to perform this operation
        price = self.stocks_data.get_price(stock_name, date)
        self.budget = (int((self.budget + price * quantity) * 100))/100
        self.stocks_owned[stock_name] -= quantity

    def add_to_budget(self, quantity):
        self.budget += quantity

    def get_budget(self):
        return self.budget

    def how_many_stocks(self, stock_name):
        if stock_name in self.stocks_owned:
            return self.stocks_owned[stock_name]
        return 0

    def save_to_file(self, date):
        data = {'stocks_owned': dict(self.stocks_owned), 'budget': self.budget, 'date': date}
        save_file = open('saves/save.json', 'w')
        dump(data, save_file)
        save_file.close()

    def sell_all(self, date):
        for stock in self.stocks_owned:
            self.sell_stocks(stock, self.how_many_stocks(stock), date)

    def save_score(self, date):
        date_played = str(datetime.now())[0:-7].replace(' ', '_').replace(':', '-')
        data = {'budget': self.budget, 'date': date, 'date_played': date_played}
        score_file = open('saves/score' + date_played + '.json', 'w')
        dump(data, score_file)
        score_file.close()

    def load_from_file(self):
        save_file = open('saves/save.json', 'r')
        data = load(save_file)
        save_file.close()
        self.stocks_owned = defaultdict(lambda: 0, data['stocks_owned'])
        self.budget = data['budget']
        return data['date']
