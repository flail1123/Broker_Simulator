import build_path
from unittest.mock import Mock, patch, MagicMock
from stock_listbox import *
from stocks_data import StocksData
from base_def import *


def test_init():
    root = MagicMock()
    stocks_data = StocksData()
    stocks_data.load_stock_data()

    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        stock_listbox = StockListbox(root, stocks_data, 5, 10, 3, 5, Mock())
        assert (stock_listbox.available_stock == [])

def test_update():
    root = MagicMock()
    stocks_data = StocksData()
    stocks_data.load_stock_data()

    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        stock_listbox = StockListbox(root, stocks_data, 5, 10, 3, 5, Mock())
        new_stock = ['AAPL']
        lost_stock = []
        stock_listbox.update(new_stock, lost_stock)
        assert stock_listbox.available_stock == ['AAPL']

        new_stock = ['AJG']
        lost_stock = ['AAPL']
        stock_listbox.update(new_stock, lost_stock)
        assert stock_listbox.available_stock == ['AJG']
