import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from major_indexes_graph import *

def test_major_indexes_graph():
    with patch('major_indexes_graph.MajorIndexesGraph.create_calendars') as create_calendars:
        create_calendars.return_value = MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        with patch('major_indexes_graph.MajorIndexesGraph.create_graph') as create_graph:
            create_graph.return_value = MagicMock(), MagicMock(), MagicMock()
            statistics_page = MagicMock()
            major_indexes_graph = MajorIndexesGraph(statistics_page)
            major_indexes_graph.display()
            assert major_indexes_graph.on_display
            major_indexes_graph.hide()
            assert not major_indexes_graph.on_display

            major_indexes_graph.update_graph("djia")
            assert major_indexes_graph.index == "djia"
            major_indexes_graph.update_graph("s_and_p500")
            assert major_indexes_graph.index == "s_and_p500"

            assert major_indexes_graph.date_from <= major_indexes_graph.date_to
            major_indexes_graph.submit_date()
            major_indexes_graph.date_from_calendar.selection_get.assert_called_once()
            major_indexes_graph.date_to_calendar.selection_get.assert_called_once()
