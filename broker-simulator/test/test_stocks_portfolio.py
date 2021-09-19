import build_path
import datetime as dt
from stocks_data import StocksData
from stocks_portfolio import StocksPortfolio, TransactionError


def test_buy_sell():
    stocks_data = StocksData()
    stocks_portfolio = StocksPortfolio(stocks_data, 2000)

    stocks_portfolio.add_to_budget(-1 * stocks_portfolio.get_budget() + 500)     #set budget to 500
    stocks_portfolio.buy_stocks('PLD', 10, dt.date(2016, 10, 10))
    assert stocks_portfolio.get_budget() < 1
    assert stocks_portfolio.how_many_stocks('PLD') == 10

    stocks_portfolio.sell_stocks('PLD', 10, dt.date(2016, 10, 10))
    assert stocks_portfolio.get_budget() == 500
    assert stocks_portfolio.how_many_stocks('PLD') == 0
