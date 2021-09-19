from base_def import *
from stocks_data import StocksData
from events_data import EventsData
from tkinter import messagebox
from navigation import Navigation
from PIL import ImageTk, Image
import pygame

# screen size variables
min_width = 800
min_height = 600
min_hd_width = 1360
min_hd_height = 768
min_size_ratio = 1
max_size_ratio = 2.5


class ScreenSetup:
    def create_screen_res(self):
        if self.screen_width < min_width or \
                self.screen_height < min_height or \
                self.screen_width / self.screen_height < min_size_ratio or \
                self.screen_width / self.screen_height > max_size_ratio:
            screen_res = ScreenRes.UNSUPPORTED
        elif self.screen_width < min_hd_width or self.screen_height < min_hd_height:
            screen_res = ScreenRes.SMALL
        else:
            screen_res = ScreenRes.HD
        return screen_res

    def check_if_screen_is_unsupported(self, root):
        if self.screen_res == ScreenRes.UNSUPPORTED:
            root.withdraw()
            messagebox.showerror("Error", "This screen resolution is not supported")
            root.destroy()
            exit(1)

    def __init__(self, root):
        root.title("Broker Simulator")
        # self.screen_width = 2000
        # self.screen_height = 1200
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        # root.attributes('-type', 'dialog')  # To make window floating in i3

        self.screen_res = self.create_screen_res()
        self.check_if_screen_is_unsupported(root)

        root.attributes('-fullscreen', True)
        root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        # root.iconbitmap('images/icon.ico')

    def get_screen_info(self):
        return self.screen_res, self.screen_width, self.screen_height


class App:
    def __init__(self, root, debug=False):
        self.stocks_data = StocksData()
        self.events_data = EventsData()

        self.root = root
        self.screen_setup = ScreenSetup(self.root)
        screen_res, screen_width, screen_height = self.screen_setup.get_screen_info()
        background_photo_with_logo = ImageTk.PhotoImage(
            Image.open('images/main-bckg-with-logo.png').resize((screen_width, screen_height)))
        background_photo_with_logo_label = Label(master=self.root, image=background_photo_with_logo, borderwidth=0)

        background_photo = ImageTk.PhotoImage(
            Image.open('images/main-bckg.png').resize((screen_width, screen_height)))
        background_photo_label = Label(master=self.root, image=background_photo, borderwidth=0)

        background_photo_scoreboard = ImageTk.PhotoImage(
            Image.open('images/background_scoreboard.png').resize((screen_width, screen_height)))
        background_photo_scoreboard_label = Label(master=self.root, image=background_photo_scoreboard,
                                                  borderwidth=0)
        background_photo_statistics = ImageTk.PhotoImage(
            Image.open('images/background_statistics.png').resize((screen_width, screen_height)))
        background_photo_statistics_label = Label(master=self.root, image=background_photo_statistics,
                                                  borderwidth=0)

        metallic_black = ImageTk.PhotoImage(Image.open('images/metallic-black.jpg'))
        metallic_yellow = ImageTk.PhotoImage(Image.open('images/metallic-yellow.jpg'))

        self.navigation = Navigation(self.root, self.stocks_data, self.events_data,
                                     (screen_res, screen_width, screen_height,
                                      background_photo_with_logo_label, background_photo_label,
                                      background_photo_scoreboard_label, background_photo_statistics_label,
                                      metallic_yellow, metallic_black))
        if not debug:
            self.root.mainloop()


if __name__ == '__main__':
    App(Tk())
