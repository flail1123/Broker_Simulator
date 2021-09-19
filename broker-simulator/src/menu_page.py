import base_def
import pygame


class MenuPage:

    def __init__(self, root, screen_info, navigation):
        self.root = root
        self.screen_info = screen_info
        self.navigate = navigation

        # get base screen info
        self.screen_res, self.screen_width, self.screen_height, self.background_photo_with_logo, _, _, _,\
            self.metallic_yellow, self.base_beige, _, self.font_color = screen_info

        # base visual variables setup
        self.button_width, self.button_height, self.button_distance, \
            self.button_border_width, self.font_style, self.stock_list_width = \
            base_def.create_settings(self.screen_res, self.screen_width, self.screen_height)

        # for centering menu buttons
        self.button_placement_x = int(0.50 * self.screen_width) - self.button_width / 2
        self.button_placement_y = int(0.50 * self.screen_height) - self.button_height / 2
        self.menu_buttons = self.create_menu_buttons()
        self.color_mode_button = base_def.FramedButton(self.root, lambda: self.navigate.change_color_mode(self.color_mode_button),
                                                       'COLOR MODE', self.metallic_yellow, self.button_width // 2,
                                                       self.button_height, self.font_style, self.font_color)
        self.music_button = base_def.FramedButton(self.root, self.play_music, 'Music: On', self.metallic_yellow,
                                                  self.button_width // 2, self.button_height, self.font_style,
                                                  self.font_color)

    def display(self):
        self.background_photo_with_logo.place(x=0, y=0)
        self.color_mode_button.get_frame().place(x=int(self.button_placement_x * 2),
                                                 y=int(self.button_placement_y * 0.1))
        self.music_button.get_frame().place(x=int(self.button_placement_x * 1.65),
                                            y=int(self.button_placement_y * 0.1))
        for i in range(len(self.menu_buttons)):
            half_of_buttons = len(self.menu_buttons) // 2
            self.menu_buttons[i].get_frame().place(x=self.button_placement_x, y=int(self.button_placement_y - (half_of_buttons - i)
                                                                        * (2 * self.button_distance +
                                                                           self.button_height)))

    def hide(self):
        self.background_photo_with_logo.place_forget()
        self.color_mode_button.get_frame().place_forget()
        self.music_button.get_frame().place_forget()
        for i in range(len(self.menu_buttons)):
            self.menu_buttons[i].get_frame().place_forget()

    def create_menu_buttons(self):
        buttons = []
        button_texts = ["New Simulation", "Continue Simulation", "Statistics", "Scoreboard", "Exit"]
        button_commands = [self.navigate.new_simulation, self.navigate.load_simulation, self.navigate.stats_display,
                           self.navigate.scoreboard_display, self.root.quit]
        for i in range(len(button_texts)):
            buttons.append(base_def.FramedButton(self.root, button_commands[i], button_texts[i],
                                                 self.metallic_yellow, self.button_width, self.button_height,
                                                 self.font_style, self.font_color))
        return buttons

    def play_music(self):
        self.navigate.play_music(self.music_button.get_button())
