import build_path
from unittest.mock import Mock, patch, MagicMock
from events_listbox import *
from events_data import EventsData
from base_def import *


def test_init():
    root = MagicMock()
    events_data = EventsData()

    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        events_listbox = EventsListbox(root, events_data, 5, 10, 5, Mock())
        assert (events_listbox.displayed_events == [])


def test_update():
    root = MagicMock()
    events_data = EventsData()

    with patch('base_def.create_settings') as create_settings:
        create_settings.return_value = 100, 50, 10, 3, MagicMock(), 28
        events_listbox = EventsListbox(root, events_data, 5, 10, 5, Mock())

        new_events = ['event event']
        events_listbox.update(new_events)
        assert events_listbox.displayed_events == ['event event']

        new_events2 = ['event2 event2']
        events_listbox.update(new_events2)
        assert events_listbox.displayed_events == ['event event', 'event2 event2']
