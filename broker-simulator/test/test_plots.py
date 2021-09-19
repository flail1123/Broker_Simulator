from tkinter import IntVar
import build_path
from plots import *
from stocks_data import *
from base_def import *
from datetime import *
from unittest.mock import Mock, patch, MagicMock


def test_stock_difference():
    stocks_data = Mock()
    stocks_data.get_available_stocks.return_value = ['AAA', 'AAB', 'AAC', 'AAD']
    available_stock = ['AAB', 'AAC', 'AAD', 'AAE']

    available_stock, new_available_stock, lost_stock = stock_difference(stocks_data, available_stock, Mock())

    assert new_available_stock == ['AAA']
    assert lost_stock == ['AAE']
    assert available_stock == ['AAA', 'AAB', 'AAC', 'AAD']


def test_fig_init():
    screen_width = 1080
    fig, ax = fig_init(screen_width, Mock())

    assert fig.get_figwidth() / fig.get_figheight() == golden_ratio
    #assert fig.get_linewidth() == fig_border_thickness


def test_stocks_init():
    stock_listbox = Mock()
    stock_listbox.selected_stock.return_value = ['AAA', 'ABC', 'DDD']
    stocks_data = Mock()
    stocks_data.get_available_stocks.return_value = ['AAA', 'ABC', 'DDD', 'BBB', 'XXX']

    stocks_list, available_stock = stocks_init(stock_listbox, stocks_data, Mock())

    assert stocks_list == ['AAA', 'ABC', 'DDD']
    assert available_stock == ['AAA', 'ABC', 'DDD', 'BBB', 'XXX']


def test_update_stock_list():
    stock_list = ['AAA', 'ABC']
    stock_listbox = Mock()
    stock_listbox.selected_stock.return_value = ['AAA', 'ABC', 'DDD']

    stock_list = update_stock_list(stock_list, stock_listbox)

    assert stock_list == stock_listbox.selected_stock()


def test_update_dates():
    stocks_data = StocksData()
    stocks_data.load_stock_data()
    date_string = Mock()
    date_to = date(2015, 12, 13)    # poniedziałek
    number_of_days_to_display = 60
    new_date_to, date_from = update_dates(date_to, number_of_days_to_display, date_string, stocks_data)

    assert new_date_to == (date_to + timedelta(days=1))
    assert date_from == new_date_to - timedelta(days=number_of_days_to_display)

    date_to = date(2015, 12, 18)    # piątek
    new_date_to, date_from = update_dates(date_to, number_of_days_to_display, date_string, stocks_data)

    assert new_date_to == (date_to + timedelta(days=3))
    assert date_from == new_date_to - timedelta(days=number_of_days_to_display)

    date_to = date(2015, 12, 19)    # sobota
    new_date_to, date_from = update_dates(date_to, number_of_days_to_display, date_string, stocks_data)

    assert new_date_to == (date_to + timedelta(days=2))
    assert date_from == new_date_to - timedelta(days=number_of_days_to_display)

    date_to = date(2014, 12, 24)    # boże narodzenie
    new_date_to, date_from = update_dates(date_to, number_of_days_to_display, date_string, stocks_data)

    assert new_date_to == (date_to + timedelta(days=2))
    assert date_from == new_date_to - timedelta(days=number_of_days_to_display)


def test_update_graph():
    fig, ax = fig_init(1080, True)
    stock_list = ['AAA', 'BBB']
    prices_in_time = [['2014-10-20', 80.80], ['2014-10-21', 90.00], ['2014-10-22', 92.20]]

    update_graph(ax, stock_list, prices_in_time, True, True)
    assert ax.get_ylim()[0] == 0
