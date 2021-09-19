import pandas as pd
import datetime as dt


def date_of_str(date_str):
    if '-' in date_str:
        result_date = [int(x) for x in date_str.split('-')]
    else:
        result_date = [int(x) for x in date_str.split(' ')]
    return dt.date(result_date[2], result_date[1], result_date[0])


class EventsData:

    def __init__(self):
        self.data = pd.read_csv('datasets/event_data.csv')
        self.data['str'] = '----' + self.data['date'] + '---- ' + self.data['dsc']
        self.data['date'] = self.data['date'].apply(date_of_str)
        self.displayed_events = []  # str column

    def get_events_to_date(self, date_to):
        res = self.data.loc[self.data['date'] <= date_to]
        return res['str']

    def update_displayed(self, to_display):
        self.displayed_events = to_display

    def get_displayed_events(self):
        return self.displayed_events
