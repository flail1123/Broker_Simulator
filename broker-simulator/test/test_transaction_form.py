import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from transaction_form import TransactionForm
from navigation import *
from datetime import date
from stocks_data import StocksData
from stocks_portfolio import StocksPortfolio

def test_transaction_form():
    root = MagicMock()

    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        with patch('PIL.Image.open') as image_open:
            image_open.return_value = MagicMock()
            with patch('PIL.ImageTk.PhotoImage') as photo_image:
                photo_image.return_value = MagicMock()
                with patch('transaction_form.TransactionForm.create_labels') as create_labels:
                    create_labels.return_value = Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
                    with patch('transaction_form.TransactionForm.create_scales') as create_scales:
                        create_scales.return_value = MagicMock(), MagicMock()
                        with patch('tkinter.Listbox.curselection') as curselection:
                            curselection.return_value = [0]
                            with patch('tkinter.Listbox.get') as get_listbox:
                                get_listbox.return_value = "AAL: American Airlines (210$)"
                                with patch('tkinter.Text.get') as get_text:
                                    get_text.return_value = "A"
                                    stock_data = StocksData()
                                    transaction_form = TransactionForm(root, (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
                                                                       Mock(), stock_data, StocksPortfolio(stock_data, 2000))
                                    current_date = date(2014, 12, 16)
                                    assert not transaction_form.on_display
                                    transaction_form.hide()
                                    assert not transaction_form.on_display
                                    transaction_form.display(current_date)
                                    assert transaction_form.on_display
                                    assert len(transaction_form.stock_list) != 0
                                    transaction_form.filter_companies_listbox()
                                    transaction_form.update_my_stock_listbox('AAL')
                                    transaction_form.buy_stock()
                                    transaction_form.buy_scale.get.assert_called_once()

                                    transaction_form.sell_stock()
                                    transaction_form.sell_scale.get.assert_called_once()

                                    transaction_form.choose_amount_to_buy(30)
                                    transaction_form.amount_to_pay.set.assert_called_once()

                                    transaction_form.choose_amount_to_sell(30)
                                    transaction_form.amount_to_receive.set.assert_called_once()






test_transaction_form()

