import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from simulation_page import *
from navigation import *


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def test_simulation_page():
    root = MagicMock()
    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        with patch('simulation_page.SimulationPage.create_graph_filters') as graph_filters:
            graph_filters.return_value = Mock(), Mock(), Mock()
            with patch('tkinter.Variable'):
                with patch('plots.draw_graph') as draw_graph:
                    draw_graph.return_value = Mock(), Mock()
                    simulation_page = SimulationPage(root, (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
                                                     Mock(), Mock(), Mock(), Mock())

                    assert (simulation_page.paused == simulation_page.get_paused())

                    assert (simulation_page.paused == True and simulation_page.on_display == False)
                    simulation_page.display()
                    assert (simulation_page.paused == False and simulation_page.on_display == True)

                    simulation_page.pause_unpause()
                    assert (simulation_page.paused == True and simulation_page.on_display == True)
                    simulation_page.pause_unpause()
                    assert (simulation_page.paused == False and simulation_page.on_display == True)

                    speed = simulation_page.time_speed
                    simulation_page.change_time_speed()
                    assert (simulation_page.time_speed > speed)

                    simulation_page.hide()
                    assert (simulation_page.on_display == False)
