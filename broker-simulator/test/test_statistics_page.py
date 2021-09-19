import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from statistics_page import *
from major_indexes_graph import MajorIndexesGraph

def test_statistics_page():
    root = MagicMock()
    with patch('base_def.create_settings') as create_settings:
        with patch('statistics_page.StatisticsPage.create_graphs') as create_graphs:
            create_graphs.return_value = MagicMock(), MagicMock()
            create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
            statistics_page = StatisticsPage(root, (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()), Mock(), MagicMock())
            statistics_page.display()
            statistics_page.graph_1.display.assert_called_once()
            assert statistics_page.on_display
            statistics_page.hide()
            statistics_page.graph_1.hide.assert_called_once()
            assert not statistics_page.on_display
