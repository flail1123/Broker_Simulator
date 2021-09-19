import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from prices_in_time_graph import *

def test_prices_in_time_graph():
    with patch('prices_in_time_graph.PricesInTimeGraph.create_calendars') as create_calendars:
        create_calendars.return_value = MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        with patch('prices_in_time_graph.PricesInTimeGraph.create_graph') as create_graph:
            create_graph.return_value = MagicMock(), MagicMock(), MagicMock()
            statistics_page = MagicMock()
            prices_in_time_graph = PricesInTimeGraph(statistics_page)
            prices_in_time_graph.display()
            assert prices_in_time_graph.on_display
            prices_in_time_graph.hide()
            assert not prices_in_time_graph.on_display

            prices_in_time_graph.update_graph("all sectors")
            assert prices_in_time_graph.sector == "all sectors"
            prices_in_time_graph.update_graph("Health Care")
            assert prices_in_time_graph.sector == "Health Care"

            assert prices_in_time_graph.date_from <= prices_in_time_graph.date_to
            prices_in_time_graph.submit_date()
            prices_in_time_graph.date_from_calendar.selection_get.assert_called_once()
            prices_in_time_graph.date_to_calendar.selection_get.assert_called_once()