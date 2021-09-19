import build_path
from unittest.mock import Mock, patch, MagicMock
from base_def import ScreenRes
from navigation import *
import tkinter


# def test_navigation_create_menu_buttons():
#     root = MagicMock()
#     with patch('base_def.create_settings') as create_settings:
#         create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
#         with patch('navigation.Navigation.create_subpages') as create_subpages:
#             create_subpages.return_value = 100, 50, 10, 3, MagicMock()
#             navigation = Navigation(root, Mock(), (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock()))
#             assert hasattr(navigation, 'menu_buttons')
#             assert len(navigation.menu_buttons) == 5
#             for button in navigation.menu_buttons:
#                 assert type(button) is tkinter.Frame


# def test_navigation_mocked_create_menu_buttons():
#     root = MagicMock()
#     with patch('base_def.create_settings') as create_settings:
#         create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
#         with patch('navigation.Navigation.create_subpages') as create_subpages:
#             create_subpages.return_value = 100, 50, 10, 3, MagicMock()
#             with patch('navigation.Navigation.create_menu_buttons') as create_menu_buttons:
#                 create_menu_buttons.return_value = [Mock(), Mock(), Mock(), Mock(), Mock()]
#                 navigation = Navigation(root, Mock(), (ScreenRes.HD, 1300, 1000, Mock(), Mock(), Mock(), Mock()))
#                 # check if buttons have been placed
#                 for button in navigation.menu_buttons:
#                     button.place.assert_called_once()
#                 assert hasattr(navigation, 'back_btn')
#                 assert type(navigation.back_btn) is tkinter.Frame
#
#                 navigation.menu_hide()
#                 for button in navigation.menu_buttons:
#                     button.place_forget.assert_called_once()
