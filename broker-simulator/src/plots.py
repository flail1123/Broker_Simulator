import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

axis_color = "#E8E9C9"
axis_color_dark = '#cbcca9'
golden_ratio = 1.61803398875
# fig_size = 6
fig_color = "#85BB65"
fig_color_dark = "#5e9040"
fig_border_color = "#3E3E3C"
fig_border_thickness = 4


def fig_init(screen_width, dark_mode):
    fig_size = int(screen_width / 300)
    if not dark_mode:
        fig, ax = plt.subplots(figsize=(fig_size * golden_ratio, fig_size),
                               facecolor=fig_color, edgecolor=fig_border_color,
                               linewidth=fig_border_thickness, tight_layout={"pad": 3})
    else:
        fig, ax = plt.subplots(figsize=(fig_size * golden_ratio, fig_size),
                               facecolor=fig_color_dark, edgecolor=fig_border_color,
                               linewidth=fig_border_thickness, tight_layout={"pad": 3})
    return fig, ax


def stocks_init(stock_listbox, stocks_data, date):
    stock_list = stock_listbox.selected_stock()

    available_stock = stocks_data.get_available_stocks(date)
    stock_listbox.update(available_stock, [])

    return stock_list, available_stock


def stock_difference(stocks_data, available_stock, date):
    current_available_stock = stocks_data.get_available_stocks(date)
    new_available_stock = np.setdiff1d(current_available_stock, available_stock)
    lost_stock = np.setdiff1d(available_stock, current_available_stock)

    return current_available_stock, new_available_stock, lost_stock,


def event_difference(events_data, date):
    current_events = events_data.get_displayed_events()
    new_events = events_data.get_events_to_date(date)
    new_to_display = list(set(new_events) - set(current_events))
    events_data.update_displayed(new_events)
    return new_to_display


def update_stock_list(stock_list, stock_listbox):
    selected_stock = stock_listbox.selected_stock()
    if stock_list != selected_stock:
        stock_list = selected_stock
    return stock_list


def update_dates(date_to, number_of_days_to_display, date_string, stocks_data):
    date_to += dt.timedelta(days=1)
    while not stocks_data.date_in_database(date_to):
        date_to += dt.timedelta(days=1)

    date_from = date_to - dt.timedelta(days=number_of_days_to_display)
    date_string.set(date_to.strftime("%Y %m %d"))
    return date_to, date_from


def update_graph(ax, stock_list, prices_in_time, scale_from_zero, dark_mode):
    ax.clear()
    ax.set(xlabel='Date', ylabel='Open ($)')
    if not dark_mode:
        ax.set_facecolor(axis_color)
    else:
        ax.set_facecolor(axis_color_dark)
    ax.grid()
    for j in range(len(stock_list)):
        ax.plot(prices_in_time[j][0], prices_in_time[j][1], label=stock_list[j])

    if scale_from_zero:
        ax.set_ylim(ymin=0)

    if stock_list:
        ax.legend(framealpha=1.0, loc='upper left')


def draw_graph(root, stocks_data, events_data, stock_listbox, events_listbox, date_to, number_of_days_to_display,
               interval, date_string, scale_graph_from_zero, screen_width, dark_mode):
    fig, ax = fig_init(screen_width, dark_mode)

    stock_list, available_stock = stocks_init(stock_listbox, stocks_data, date_to)

    def animate(i):
        nonlocal date_to, available_stock, stock_list

        stock_list = update_stock_list(stock_list, stock_listbox)

        date_to, date_from = update_dates(date_to, number_of_days_to_display.get(), date_string, stocks_data)

        # List of pairs - 'date' + 'stock price'
        prices_in_time = stocks_data.get_prices_in_time(stock_list, date_from, date_to)

        update_graph(ax, stock_list, prices_in_time, scale_graph_from_zero.get(), dark_mode)

        available_stock, new_available_stock, lost_stock = stock_difference(stocks_data, available_stock, date_to)
        new_events = event_difference(events_data, date_to)

        # dodaje new_avalible_stock do stock_listboxa i wywalamy lost_stock
        stock_listbox.update(new_available_stock, lost_stock)
        events_listbox.update(new_events)

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    ani = animation.FuncAnimation(fig, animate, interval=interval)

    return ani, canvas
