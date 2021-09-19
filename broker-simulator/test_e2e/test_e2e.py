from threading import Thread
import unittest
from tkinter import Tk, Toplevel
from PIL import ImageTk, Image
from time import sleep

import build_path
from app import App
from base_def import *
from datetime import *
from simulation_page import *
from stocks_data import date_of_str
from transaction_form import *


def run_test_game_start(app):
    sleep(0.1)  # To make sure everything initialized

    # Check if navigation and menu page initialized correctly
    navigation = app.navigation
    assert navigation
    assert 'menu' in navigation.subpages
    menu_page = navigation.subpages['menu']
    assert menu_page

    # Initialize and check simulation page
    assert not ('simulation' in navigation.subpages)
    menu_page.menu_buttons[0].button.invoke()  # Creating new simulation
    assert 'simulation' in navigation.subpages
    simulation = navigation.subpages['simulation']
    assert simulation


    # Check basic simulation properties
    assert simulation.on_display
    assert navigation.stocks_portfolio.budget == base_def.default_starting_budget
    assert len(navigation.stocks_portfolio.stocks_owned) == 0
    assert simulation.current_date >= base_def.min_date
    assert simulation.current_date <= base_def.max_date

    sleep(1)

    assert len(simulation.stock_listbox.available_stock) > 0
    assert len(simulation.stock_listbox.available_stock) == simulation.stock_listbox.listbox.size()
    assert len(simulation.stock_listbox.selected_stock()) == 0

    # Check color changes
    assert navigation.color_mode_flag == 0
    menu_page.color_mode_button.button.invoke()
    assert navigation.color_mode_flag == 1
    menu_page.color_mode_button.button.invoke()
    assert navigation.color_mode_flag == 0

    simulation.back_btn.button.invoke()
    menu_page.menu_buttons[4].button.invoke()  # Exit game



def run_test_game_speed(app):
    sleep(0.01)  # To make sure everything initialized

    navigation = app.navigation
    menu_page = navigation.subpages['menu']
    menu_page.menu_buttons[0].button.invoke()  # Creating new simulation
    simulation = navigation.subpages['simulation']

    # Initialize animation (which updates date)
    ani = simulation.graph_animation
    ani._init_draw()

    # Check time values
    start_date = simulation.date_string.get()
    assert start_date
    assert ani.event_source.interval == simulation.base_interval // simulation.time_speed
    assert simulation.time_speed == default_time_speed

    # Manipulate time
    simulation.change_time_speed_button.button.invoke()
    assert simulation.time_speed > default_time_speed
    assert ani.event_source.interval == simulation.base_interval // simulation.time_speed

    # Pause unpause
    assert not simulation.paused
    simulation.pause_unpause_button.button.invoke()
    assert simulation.paused

    pause_date = simulation.date_string.get()
    sleep(0.2)  # Make sure that time is not changing
    assert pause_date == simulation.date_string.get()

    simulation.pause_unpause_button.button.invoke()
    assert not simulation.paused

    # Check if time has passed
    sleep(0.6)
    assert start_date != simulation.date_string.get()

    simulation.back_btn.button.invoke()
    menu_page.menu_buttons[4].button.invoke()  # Exit game


def transaction_buy(transaction, amount):
    transaction.companies_listbox.event_generate("<<ListboxSelect>>")
    transaction.buy_scale.set(amount)
    transaction.choose_amount_to_buy(amount)
    transaction.buy_button.button.invoke()


def transaction_sell(transaction, amount):
    transaction.my_stock_listbox.event_generate("<<ListboxSelect>>")
    transaction.sell_scale.set(amount)
    transaction.choose_amount_to_sell(amount)
    transaction.sell_button.button.invoke()


def run_test_buy_sell_static(app):
    sleep(0.01)  # To make sure everything initialized

    navigation = app.navigation
    menu_page = navigation.subpages['menu']
    menu_page.menu_buttons[0].button.invoke()  # Creating new simulation
    simulation = navigation.subpages['simulation']
    ani = simulation.graph_animation
    ani._init_draw()

    # Go to form
    simulation.to_form_btn.button.invoke()
    transaction = navigation.subpages['transaction']
    assert transaction

    # Buy stocks
    transaction_buy(transaction, 5)

    # assert navigation.stocks_portfolio.budget < base_def.default_starting_budget
    assert navigation.stocks_portfolio.budget > 0
    assert len(navigation.stocks_portfolio.stocks_owned) == 1
    assert 'AAL' in navigation.stocks_portfolio.stocks_owned.keys()
    assert navigation.stocks_portfolio.stocks_owned['AAL'] == 5

    # Sell some stocks
    lowest_budget = navigation.stocks_portfolio.budget
    transaction_sell(transaction, 2)

    assert navigation.stocks_portfolio.budget < base_def.default_starting_budget
    assert navigation.stocks_portfolio.budget > lowest_budget
    assert 'AAL' in navigation.stocks_portfolio.stocks_owned

    # Sell all stocks
    transaction_sell(transaction, 3)

    assert navigation.stocks_portfolio.budget == base_def.default_starting_budget
    assert navigation.stocks_portfolio.stocks_owned['AAL'] == 0

    transaction.back_to_sim_btn.button.invoke()
    simulation.back_btn.button.invoke()
    menu_page.menu_buttons[4].button.invoke()  # Exit game


def run_test_buy_sell_many_times(app):
    sleep(0.01)  # To make sure everything initialized

    navigation = app.navigation
    menu_page = navigation.subpages['menu']
    menu_page.menu_buttons[0].button.invoke()  # Creating new simulation
    simulation = navigation.subpages['simulation']
    ani = simulation.graph_animation
    ani._init_draw()
    simulation.to_form_btn.button.invoke()
    transaction = navigation.subpages['transaction']
    assert transaction

    prev_budget = base_def.default_starting_budget

    # Buy stocks
    for i in range(10):
        transaction_buy(transaction, 1)
        sleep(0.02)
        assert navigation.stocks_portfolio.budget < prev_budget
        assert navigation.stocks_portfolio.stocks_owned['AAL'] == i + 1
        prev_budget = navigation.stocks_portfolio.budget

    prev_budget = 0

    # Sell stocks
    for i in range(10):
        transaction_sell(transaction, 1)
        sleep(0.02)
        print(i)
        assert navigation.stocks_portfolio.budget > prev_budget
        assert navigation.stocks_portfolio.stocks_owned['AAL'] == 9 - i
        prev_budget = navigation.stocks_portfolio.budget

    assert navigation.stocks_portfolio.budget > base_def.default_starting_budget - 1
    assert navigation.stocks_portfolio.budget < base_def.default_starting_budget + 1
    assert navigation.stocks_portfolio.stocks_owned['AAL'] == 0

    transaction.back_to_sim_btn.button.invoke()
    simulation.back_btn.button.invoke()
    menu_page.menu_buttons[4].button.invoke()  # Exit game


def run_test_move_around(app):
    sleep(0.01)  # To make sure everything initialized

    navigation = app.navigation
    menu_page = navigation.subpages['menu']

    menu_page.menu_buttons[0].button.invoke()  # Creating new simulation
    simulation = navigation.subpages['simulation']
    assert simulation
    simulation.back_btn.button.invoke()

    menu_page.menu_buttons[2].button.invoke()  # Statistics
    statistics = navigation.subpages['statistics']
    assert statistics
    statistics.back_button.button.invoke()

    menu_page.menu_buttons[3].button.invoke()  # Scoreboard
    scoreboard = navigation.subpages['scoreboard']
    assert scoreboard
    scoreboard.back_button.button.invoke()

    menu_page.menu_buttons[4].button.invoke()  # Exit game


def run_test_wrapper(run_test_function):
    app = App(Toplevel(), debug=True)
    t = Thread(target=run_test_function, args=(app,))
    t.start()
    app.root.mainloop()
    t.join()


def test_game_start():
    run_test_wrapper(run_test_game_start)


def test_game_speed():
    run_test_wrapper(run_test_game_speed)


def test_buy_sell_static():
    run_test_wrapper(run_test_buy_sell_static)


def test_buy_sell_many_times():
    run_test_wrapper(run_test_buy_sell_many_times)


def test_move_around():
    run_test_wrapper(run_test_move_around)
