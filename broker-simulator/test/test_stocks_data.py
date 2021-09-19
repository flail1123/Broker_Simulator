import build_path
import datetime as dt
from stocks_data import StocksData, date_of_str


def test_date_of_str():
    assert (date_of_str('2000-01-01') == dt.date(2000, 1, 1))
    assert (date_of_str('2010-10-10') == dt.date(2010, 10, 10))
    assert (date_of_str('2018-12-12') == dt.date(2018, 12, 12))
    assert (date_of_str('2018-07-30') == dt.date(2018, 7, 30))
    assert (date_of_str('2021-02-28') == dt.date(2021, 2, 28))


def test_create_dictionary_of_abbreviations():
    test_abbreviations = ['YUM', 'CPA', 'MNCL', 'PRCH', 'ACM']
    result_names = ['Yum! Brands', 'Copa Holdings', 'Monocle Acquisition', 'Porch Group', 'Aecom']
    stocks_data = StocksData()
    for i in range(len(test_abbreviations)):
        assert stocks_data.abbreviations[test_abbreviations[i]] == result_names[i]


def test_get_prices_in_time():
    stocks_data = StocksData()
    stocks_data.load_stock_data()
    stock_list = ['FRT']
    date_from = dt.date(2017, 10, 4)
    date_to = dt.date(2017, 10, 9)
    result = stocks_data.get_prices_in_time(stock_list, date_from, date_to, 'open')
    expected = ([dt.date(2017, 10, 4), dt.date(2017, 10, 5), dt.date(2017, 10, 6), dt.date(2017, 10, 9)],
                [124.67, 125.43, 125.29, 125.8])
    assert result[0][0].values.tolist() == expected[0]
    assert result[0][1].values.tolist() == expected[1]


def test_get_price():
    stocks_data = StocksData()
    assert stocks_data.get_price('FRT', dt.date(2017, 10, 4)) == 124.67
    assert stocks_data.get_price('FRT', dt.date(2017, 10, 4), 'close') == 125.13


def test_get_available_stocks():
    stocks_data = StocksData()
    date = dt.date(2017, 10, 9)
    assert len(stocks_data.get_available_stocks(date)) == 504
    date = dt.date(2012, 10, 9)
    assert len(stocks_data.get_available_stocks(date)) == 0
    date = dt.date(2013, 5, 9)
    assert len(stocks_data.get_available_stocks(date)) == 477
