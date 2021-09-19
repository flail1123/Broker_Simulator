import base_def
from major_indexes_graph import MajorIndexesGraph
from prices_in_time_graph import PricesInTimeGraph

class StatisticsPage:
    # def create_graph_1(self):
    #     fig, ax = fig_init(self.screen_width, False)
    #     canvas = FigureCanvasTkAgg(fig, self.root)
    #     return canvas

    def create_graphs(self):
        return MajorIndexesGraph(self), PricesInTimeGraph(self)

    def __init__(self, root, screen_info, navigation, stocks_data):
        self.current_graph = 1
        self.on_display = False
        self.root = root
        self.stocks_data = stocks_data
        self.navigate = navigation
        self.screen_res, self.screen_width, self.screen_height, _, _, _,\
            self.background_photo_statistics_label, self.metallic_yellow, \
            self.base_beige, self.base_color, self.font_color = screen_info
        self.button_width, self.button_height, self.button_distance, self.button_border_width, self.font_style, \
            self.stock_list_width = base_def.create_settings(self.screen_res, self.screen_width, self.screen_height)
        self.dark_mode = (self.font_color == "white")
        self.back_button, self.back_button_x, self.back_button_y = self.create_back_button()
        self.list_placement_x = int(base_def.pad_horizontal * self.screen_width)
        self.list_placement_y = int(base_def.pad_vertical * self.screen_height)

        self.graph_1, self.graph_2 = self.create_graphs()

    def display(self):
        self.background_photo_statistics_label.place(x=0, y=0)
        self.back_button.get_frame().place(x=self.back_button_x, y=self.back_button_y)
        self.on_display = True
        if self.current_graph == 1:
            self.graph_1.display()
        else:
            self.graph_2.display()

    def hide(self):
        self.background_photo_statistics_label.place_forget()
        self.back_button.get_frame().place_forget()
        if self.current_graph == 1:
            self.graph_1.hide()
        else:
            self.graph_2.hide()
        self.on_display = False

    def create_back_button(self):
        # for back button in upper left corner
        back_button_x = int(base_def.pad_horizontal * self.screen_width)
        back_button_y = int(self.button_height)

        back_button = base_def.FramedButton(self.root, self.navigate.statistics_to_main, "Back to menu",
                                            self.metallic_yellow,  int(self.button_width / 2), self.button_height,
                                            self.font_style, self.font_color)
        return back_button, back_button_x, back_button_y