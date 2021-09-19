import pandas as pd
import datetime as dt
import numpy as np
import re


def date_of_str(date_str):
    if '/' in date_str:
        month, day, year = (int(x) for x in date_str.split('/'))
        result_date = [year, month, day]
    elif '-' in date_str:
        result_date = [int(x) for x in date_str.split('-')]
    else:
        result_date = [int(x) for x in date_str.split(' ')]
    return dt.date(result_date[0], result_date[1], result_date[2])


class StocksData:

    def __init__(self):
        self.path_to_stocks_data = 'datasets/all_stocks_5yr.csv'
        self.path_to_abbreviations = 'datasets/stock_ticker_symbols.txt'
        self.path_to_nasdaqc = 'datasets/nasdaqc.csv'
        self.path_to_djia = 'datasets/djia.csv'
        self.path_to_s_and_p500 = 'datasets/s&p500.csv'
        self.path_to_vix = 'datasets/vix.csv'
        self.path_to_sector_data = 'datasets/sectors.csv'

        self.abbreviations = {}
        self.create_abbreviations_dict()

        self.data = None
        self.indexes = None
        self.sector_data = None
        self.load_indexes()
        self.load_stock_data()
        self.load_sector_data()

    def create_abbreviations_dict(self):
        abbreviations_file = open(self.path_to_abbreviations, 'r')
        regex = re.compile(r'^(.*) - (.*)$')
        while True:
            line = abbreviations_file.readline()
            if len(line) == 0:
                break
            abbreviation, name = regex.search(line).groups()
            self.abbreviations[abbreviation] = name

    def load_indexes(self):
        self.indexes = {"vix": pd.read_csv(self.path_to_vix), "nasdaqc": pd.read_csv(self.path_to_nasdaqc),
                        "djia": pd.read_csv(self.path_to_djia), "s_and_p500": pd.read_csv(self.path_to_s_and_p500)}
        for key in self.indexes.keys():
            self.indexes[key]['Date'] = self.indexes[key]['Date'].apply(date_of_str)

    def load_stock_data(self):
        self.data = pd.read_csv(self.path_to_stocks_data)
        self.data['date'] = self.data['date'].apply(date_of_str)

    def get_prices_in_time(self, stock_list, date_from, date_to, price_type='open'):
        dates = np.bitwise_and((date_from <= self.data['date']), (self.data['date'] <= date_to))
        results = []
        for stock in stock_list:
            general_stock_info = self.data[self.data['Name'] == stock]
            result_dates = general_stock_info['date'][dates]
            result_prices = general_stock_info[price_type][dates]
            results.append((result_dates, result_prices))
        return results

    def get_indexes(self, date_from, date_to, names_of_index):
        return self.indexes[names_of_index][(self.indexes[names_of_index]['Date'] <= date_to) & \
                (self.indexes[names_of_index]['Date'] >= date_from) & (self.indexes[names_of_index]['Open'] > 0)]\
               [["Date", "Open"]].values.tolist()

    def load_sector_data(self):
        self.sector_data = pd.read_csv(self.path_to_sector_data, usecols=['Symbol', 'Sector'])

    def get_sector_names(self):
        return self.sector_data['Sector'].unique()

    def get_stocks_name_in_sector(self, sector, date_from, date_to):
        if sector == 'all sectors':
            return np.intersect1d(self.get_available_stocks(date_from), self.get_available_stocks(date_to))
        else:
            all_stocks = np.intersect1d(self.get_available_stocks(date_from), self.get_available_stocks(date_to))
            stocks_in_sector = self.sector_data[self.sector_data['Sector'] == sector].Symbol.unique()
            return np.intersect1d(all_stocks, stocks_in_sector)

    def get_stocks_name_and_price_in_date(self, date):
        return self.data[self.data['date'] == date][["Name", "open"]].values.tolist()

    def get_price(self, stock_name, date, price_type='open'):
        precise_stock = self.data[(self.data['Name'] == stock_name) & (self.data['date'] == date)]
        return precise_stock[price_type].values[0]

    def get_available_stocks(self, date):
        return self.data[self.data['date'] == date].Name.unique()

    def is_abbreviation_correct(self, abbreviation):
        return self.abbreviations.__contains__(abbreviation)

    def get_name_for_abbreviation(self, abbreviation):
        return self.abbreviations[abbreviation]

    def date_in_database(self, date):
        return not self.data[self.data['date'] == date].empty
