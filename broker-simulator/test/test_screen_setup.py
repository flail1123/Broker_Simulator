import build_path
from app import *
from unittest.mock import Mock, patch
from base_def import ScreenRes


def test_screen_setup():
    root = Mock()
    test_cases = [(10, 20), (800, 600), (1360, 768), (1000, 100000), (3840, 2160)]
    results = [ScreenRes.UNSUPPORTED, ScreenRes.SMALL, ScreenRes.HD, ScreenRes.UNSUPPORTED, ScreenRes.HD]
    for i, (width, height) in enumerate(test_cases):
        root.winfo_screenwidth.return_value = width
        root.winfo_screenheight.return_value = height
        if results[i] == ScreenRes.UNSUPPORTED:
            with patch('app.ScreenSetup.check_if_screen_is_unsupported'):
                test = ScreenSetup(root)
        else:
            test = ScreenSetup(root)
        assert test.get_screen_info() == (results[i], width, height)
