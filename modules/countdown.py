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
        Event("Bulldog Days", datetime.datetime(year=2019, month=4, day=15), datetime.timedelta(days=3)),
        Event("orientation week begins", datetime.datetime(year=2019, month=8, day=20), datetime.timedelta(days=1)),
    ]

    def response(self, query, message):
        """
        Calculate response given input.
        :param query: text input to command.
        """
        remaining = self.time()
        if remaining is None:
            return "There are no events scheduled."
        return "There are %d weeks, %d days, %d hours, %d minutes, and %d seconds left until %s." % remaining

    def next_event(self, now: datetime.datetime) -> Event:
        """
        :return: next event in list.
        """
        for event in self.events:
            if (event.date + event.duration - now).total_seconds() > 0:
                return event
        return None

    def time(self):
        """
        Get time split into units until Bulldog Days.
        """
        now = datetime.datetime.now()
        event = self.next_event(now)
        if event is None:
            return None
        delta = event.date - now
        seconds = delta.total_seconds()
        weeks, seconds = divmod(seconds, 60*60*24*7)
        days, seconds = divmod(seconds, 60*60*24)
        hours, seconds = divmod(seconds, 60*60)
        minutes, seconds = divmod(seconds, 60)
        return weeks, days, hours, minutes, seconds, event.name
