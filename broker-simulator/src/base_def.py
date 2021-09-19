from tkinter import *
from enum import Enum
import tkinter.font as tk_font
import pygame
import pytest
from datetime import date

# button ratios
btn_small_scr_width = 0.28
btn_big_scr_width = 0.2
btn_small_scr_height = 0.4 / 7
btn_big_scr_height = 0.3 / 7
btn_small_scr_dst = 0.3 / 14
btn_big_scr_dst = 0.2 / 14
btn_small_scr_border = 3
btn_big_scr_border = 3
btn_small_scr_font = 3.5
btn_big_scr_font = 3
small_scr_stocks_display = 20
big_scr_stocks_display = 20
pad_horizontal = 0.03
pad_vertical = 0.15
list_bg_color = "#E8E9C9"
list_bg_color_dark_mode = 'LemonChiffon3'

# Game consts
default_starting_budget = 2000.0
min_date = date(2013, 2, 10)
max_date = date(2018, 2, 7)


class ScreenRes(Enum):
    HD = 0
    SMALL = 1
    UNSUPPORTED = 2


def create_settings(screen_res, screen_width, screen_height):
    if screen_res == ScreenRes.HD:
        button_width = int(btn_big_scr_width * screen_width)
        button_height = int(btn_big_scr_height * screen_height)
        button_distance = int(btn_big_scr_dst * screen_height)
        button_border_width = btn_big_scr_border
        stock_list_width = 30
        font_style = tk_font.Font(family="Segoe UI semibold", size=int(button_height // btn_big_scr_font))
    else:
        button_width = int(btn_small_scr_width * screen_width)
        button_height = int(btn_small_scr_height * screen_height)
        button_distance = int(btn_small_scr_dst * screen_height)
        button_border_width = btn_small_scr_border
        font_style = tk_font.Font(family="Segoe UI semibold", size=int(button_height / btn_small_scr_font))
        stock_list_width = 22
    return button_width, button_height, button_distance, button_border_width, font_style, stock_list_width


class FramedButton:
    default_color = "#54e4fa"
    default_border_width = 3

    def __init__(self, root, command, text, image, width, height, font, font_color, cash_button=False):
        self.cash_button = cash_button
        self.frame = Frame(root, highlightbackground="black", highlightthickness=self.default_border_width, bd=0)
        self.button = Button(self.frame, text=text, command=command, compound="c", image=image, width=width,
                             height=height, bg=self.default_color, font=font, borderwidth=0, fg=font_color)
        self.button.bind("<Button>", self.onclick_sound)
        self.button.pack()

    def get_frame(self):
        return self.frame

    def get_button(self):
        return self.button

    def onclick_sound(self, event):
        if not self.cash_button:
            sound1 = pygame.mixer.Sound("audio/click.mp3")
            pygame.mixer.Channel(1).play(sound1, loops=0)
        else:
            sound2 = pygame.mixer.Sound("audio/ka-ching.mp3")
            pygame.mixer.Channel(1).set_volume(0.1)
            pygame.mixer.Channel(1).play(sound2, loops=0)


class FramedLabel:
    default_color = "#54e4fa"
    default_border_width = 3

    def __init__(self, root, variable, image, width, height, font, font_color):
        self.frame = Frame(root, highlightbackground="black", highlightthickness=self.default_border_width, bd=0)
        self.label = Label(self.frame, textvariable=variable, compound="c", image=image, width=width,
                           height=height, bg=self.default_color, font=font, borderwidth=0, fg=font_color)
        self.label.pack()

    def get_frame(self):
        return self.frame

    def get_label(self):
        return self.label
