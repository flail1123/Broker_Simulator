import build_path
from base_def import *
from unittest.mock import Mock, patch, MagicMock
import tkinter


def test_screen_res():
    assert ScreenRes.HD != ScreenRes.SMALL != ScreenRes.UNSUPPORTED


def test_create_settings():
    with patch("tkinter.font.Font"):
        button_width, button_height, button_distance, button_border_width, font_style, stock_list_width = create_settings(ScreenRes.HD, 1400, 800)
        assert button_width == int(btn_big_scr_width * 1400)
        assert button_height == int(btn_big_scr_height * 800)
        assert button_distance == int(btn_big_scr_dst * 800)
        assert button_border_width == btn_big_scr_border

        button_width, button_height, button_distance, button_border_width, font_style, stock_list_width = create_settings(ScreenRes.SMALL, 800, 600)
        assert button_width == int(btn_small_scr_width * 800)
        assert button_height == int(btn_small_scr_height * 600)
        assert button_distance == int(btn_small_scr_dst * 600)
        assert button_border_width == btn_small_scr_border


def test_framed_button():
    root = MagicMock()
    root.__add__ = lambda a, b: 5
    command = lambda: 10
    image = Mock()
    framed_button = FramedButton(root, command, 'some text', image, 100, 50, Mock(), Mock())
    assert hasattr(framed_button, 'get_frame')
    frame = framed_button.get_frame()
    assert type(frame) is tkinter.Frame
