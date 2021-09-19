import base_def
from menu_page import MenuPage
from simulation_page import SimulationPage
from scoreboard_page import ScoreboardPage
from statistics_page import StatisticsPage
from transaction_form import TransactionForm
from stocks_portfolio import StocksPortfolio
from stocks_data import date_of_str
import pygame
import pytest

LIGHT = 0
DARK = 1


def create_color_mode_versions(screen_info):
    arg1, arg2, arg3, arg4, arg5, arg6, arg7, metallic_yellow, metallic_grey = screen_info
    screen_info_dark_mode = arg1, arg2, arg3, arg4, arg5, arg6, arg7, metallic_grey, metallic_yellow, \
        base_def.list_bg_color_dark_mode, "white"
    screen_info_light_mode = arg1, arg2, arg3, arg4, arg5, arg6, arg7, metallic_yellow, metallic_grey, \
        base_def.list_bg_color, "black"
    return screen_info_light_mode, screen_info_dark_mode


class Navigation:

    def __init__(self, root, stocks_data, events_data, screen_info):
        self.root = root
        self.screen_info = screen_info
        self.screen_info_light_mode, self.screen_info_dark_mode = create_color_mode_versions(screen_info)
        self.color_mode_flag = LIGHT
        self.music_flag = True

        self.stocks_data = stocks_data
        self.events_data = events_data
        self.stocks_portfolio = None

        pygame.mixer.init()
        pygame.mixer.Channel(0).set_volume(0.3)
        background_music = pygame.mixer.Sound("audio/melody.mp3")
        pygame.mixer.Channel(0).play(background_music, loops=-1)

        self.subpages = {'menu': MenuPage(root, self.screen_info_light_mode, self),
                         'menu_dark': MenuPage(root, self.screen_info_dark_mode, self)}
        self.subpages['menu'].display()


    def save_simulation(self):
        current_date_str = self.subpages['simulation'].date_string.get()
        self.stocks_portfolio.save_to_file(current_date_str)

    def finish_game(self):
        current_date_str = self.subpages['simulation'].date_string.get()
        self.stocks_portfolio.sell_all(date_of_str(current_date_str))
        self.stocks_portfolio.save_score(current_date_str)
        self.simulation_to_main()  # go to main menu

    # TRANSITIONING METHODS:

    def new_simulation(self):
        self.stocks_portfolio = StocksPortfolio(self.stocks_data, base_def.default_starting_budget)
        if self.color_mode_flag == LIGHT:
            self.subpages['simulation'] = SimulationPage(self.root, self.screen_info_light_mode, self, self.stocks_data, self.events_data, self.color_mode_flag) # Pycharm does not like that
            self.subpages['menu'].hide()
        else:
            self.subpages['simulation'] = SimulationPage(self.root, self.screen_info_dark_mode, self, self.stocks_data, self.events_data, self.color_mode_flag) # Pycharm does not like that
            self.subpages['menu_dark'].hide()
        self.subpages['simulation'].display()

    def load_simulation(self):
        self.stocks_portfolio = StocksPortfolio(self.stocks_data, base_def.default_starting_budget)
        date = date_of_str(self.stocks_portfolio.load_from_file())
        if self.color_mode_flag == LIGHT:
            self.subpages['simulation'] = SimulationPage(self.root, self.screen_info_light_mode, self, self.stocks_data, self.events_data, self.color_mode_flag, date) # Pycharm does not like that
            self.subpages['menu'].hide()
        else:
            self.subpages['simulation'] = SimulationPage(self.root, self.screen_info_dark_mode, self, self.stocks_data, self.events_data, self.color_mode_flag, date) # Pycharm does not like that
            self.subpages['menu_dark'].hide()
        self.subpages['simulation'].display()

    def simulation_to_main(self):
        self.subpages['simulation'].hide()
        self.subpages['simulation'].stop_animation()
        if self.color_mode_flag == LIGHT:
            self.subpages['menu'].display()
        else:
            self.subpages['menu_dark'].display()

    def scoreboard_to_main(self):
        self.subpages['scoreboard'].hide()
        if self.color_mode_flag == LIGHT:
            self.subpages['menu'].display()
        else:
            self.subpages['menu_dark'].display()

    def statistics_to_main(self):
        self.subpages['statistics'].hide()
        if self.color_mode_flag == LIGHT:
            self.subpages['menu'].display()
        else:
            self.subpages['menu_dark'].display()

    def simulation_to_transaction(self):
        if not self.subpages['simulation'].get_paused():
            self.subpages['simulation'].pause_unpause()
        if self.color_mode_flag == LIGHT:
            self.subpages['transaction'] = TransactionForm(self.root, self.screen_info_light_mode, self, self.stocks_data, self.stocks_portfolio)
        else:
            self.subpages['transaction'] = TransactionForm(self.root, self.screen_info_dark_mode, self, self.stocks_data, self.stocks_portfolio)
        current_date = date_of_str(self.subpages['simulation'].date_string.get())

        self.subpages['simulation'].hide()
        self.subpages['transaction'].display(current_date)

    def transaction_to_simulation(self):
        self.subpages['transaction'].hide()
        self.subpages['simulation'].display()

    def stats_display(self):
        if self.color_mode_flag == LIGHT:
            self.subpages['statistics'] = StatisticsPage(self.root, self.screen_info_light_mode, self, self.stocks_data)
            self.subpages['menu'].hide()
        else:
            self.subpages['statistics'] = StatisticsPage(self.root, self.screen_info_dark_mode, self, self.stocks_data)
            self.subpages['menu_dark'].hide()
        self.subpages['statistics'].display()

    def scoreboard_display(self):
        if self.color_mode_flag == LIGHT:
            self.subpages['scoreboard'] = ScoreboardPage(self.root, self.screen_info_light_mode, self, self.color_mode_flag)
            self.subpages['menu'].hide()
        else:
            self.subpages['scoreboard'] = ScoreboardPage(self.root, self.screen_info_dark_mode, self, self.color_mode_flag)
            self.subpages['menu_dark'].hide()
        self.subpages['scoreboard'].display()

    def change_color_mode(self, btn):
        if self.color_mode_flag == LIGHT:
            self.subpages['menu'].hide()
            self.subpages['menu_dark'].display()
            self.color_mode_flag = DARK
        else:
            self.subpages['menu_dark'].hide()
            self.subpages['menu'].display()
            self.color_mode_flag = LIGHT

    def play_music(self, button):
        if self.music_flag:
            pygame.mixer.Channel(0).pause()
            self.music_flag = False
            button.config(text="Music: Off")
        else:
            pygame.mixer.Channel(0).unpause()
            self.music_flag = True
            button.config(text="Music: On")
