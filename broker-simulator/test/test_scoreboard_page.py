import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import *
from scoreboard_page import *
from navigation import *
from datetime import *
import os


def test_scoreboard_page():
    root = MagicMock()
    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        with patch('scoreboard_page.ScoreboardPage.create_style_for_scoreboard') as create_style:
            create_style.return_value = MagicMock()
            scoreboard_page = ScoreboardPage(root, (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()),
                                             Mock(), Mock())
            assert scoreboard_page.records is None
            scoreboard_page.display()
            assert len(scoreboard_page.records) == len(os.listdir('saves')) - 1  # one is for current save
            scoreboard_page.highlight_row(MagicMock())
            scoreboard_page.sort_scoreboard(MagicMock())
            if len(scoreboard_page.records) > 0:
                assert type(scoreboard_page.records[0][0]) == datetime and \
                       type(scoreboard_page.records[0][1]) == int and type(scoreboard_page.records[0][2]) == datetime
            assert type(scoreboard_page.records) == list
            assert scoreboard_page.on_display
            scoreboard_page.hide()
            assert not scoreboard_page.on_display
