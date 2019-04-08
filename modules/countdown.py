from .base import Module
import datetime


class Event:
    def __init__(self, name: str, date: datetime.datetime, duration: datetime.timedelta):
        self.name = name
        self.date = date
        self.duration = duration


class Countdown(Module):
    DESCRIPTION = "Find out how little time's left until upcoming Yale events"
    events = [
        Event("Bulldog Days", datetime.datetime(year=2019, month=4, day=15, hour=14), datetime.timedelta(days=3)),
        Event("orientation week begins", datetime.datetime(year=2019, month=8, day=20), datetime.timedelta(days=1)),
    ]

    def get_event(self, name):
        for option in self.events:
            if option.name == name:
                return option
        return None

    def response(self, query, message):
        """
        Calculate response given input.
        :param query: text input to command.
        """
        if query:
            event = self.get_event(query)
            if event is None:
                return "Couldn't find the event '%s'" % query
        else:
            event = self.next_event()
        remaining = self.time(event)
        if remaining is None:
            return "There are no events scheduled."
        plurality = tuple(["is" if remaining[0] == 1 else "are"]) + tuple("" if num == 1 else "s" for num in remaining[:5])
        return "There {0} {6} week{1}, {7} day{2}, {8} hour{3}, {9} minute{4}, and {10} second{5} left until {11}.".format(*(plurality + remaining))

    def next_event(self) -> Event:
        """
        :return: next event in list.
        """
        now = datetime.datetime.now()
        for event in self.events:
            if (event.date + event.duration - now).total_seconds() > 0:
                return event
        return None

    def time(self, event):
        """
        Get time split into units until Bulldog Days.
        """
        now = datetime.datetime.now()
        if event is None:
            return None
        delta = event.date - now
        seconds = delta.total_seconds()
        weeks, seconds = divmod(seconds, 60 * 60 * 24 * 7)
        days, seconds = divmod(seconds, 60 * 60 * 24)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        return weeks, days, hours, minutes, seconds, event.name
