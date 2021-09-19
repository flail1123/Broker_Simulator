import build_path
from events_data import EventsData, date_of_str
import datetime as dt


def test_date_of_str():
    assert (date_of_str('12-02-2013') == dt.date(2013, 2, 12))
    assert (date_of_str('11-10-2010') == dt.date(2010, 10, 11))
    assert (date_of_str('12-12-2018') == dt.date(2018, 12, 12))
    assert (date_of_str('30-07-2018') == dt.date(2018, 7, 30))
    assert (date_of_str('28-02-2021') == dt.date(2021, 2, 28))


def test_get_events_to_date():
    events_data = EventsData()
    date_to = dt.date(2013, 2, 14)
    result = events_data.get_events_to_date(date_to)
    expected = "----12-02-2013---- North Korea conducts its third underground nuclear test, prompting widespread condemnation and tightened economic sanctions from the international community."
    assert result[0] == expected


def test_displayed():
    events_data = EventsData()
    to_display = ["hello"]
    events_data.update_displayed(to_display)
    assert(events_data.get_displayed_events() == to_display)
