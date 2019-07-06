from .base import Module
import datetime


class Event:
    def __repr__(self):
        remaining = self.remaining_time()
        if remaining is None:
            return "There are no events scheduled."
        plurality = tuple(["is" if remaining[0] == 1 else "are"]) + tuple("" if num == 1 else "s" for num in remaining[:5])
        # TODO: Do this formatting better
        return "There {0} {6} week{1}, {7} day{2}, {8} hour{3}, {9} minute{4}, and {10:.2f} second{5} left until {name}.".format(*(plurality + remaining),
                                                                                                                                 name=self.name)

    def remaining_time(self):
        """
        Get time split into units until Bulldog Days.
        """
        now = datetime.datetime.now()
        delta = self.date - now
        seconds = delta.total_seconds()
        weeks, seconds = divmod(seconds, 60 * 60 * 24 * 7)
        days, seconds = divmod(seconds, 60 * 60 * 24)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        return int(weeks), int(days), int(hours), int(minutes), seconds

    def __init__(self, name: str, date: datetime.datetime):
        self.name = name
        # Compensate for heroku hosting timezone
        self.date = date + datetime.timedelta(hours=4)


class Countdown(Module):
    DESCRIPTION = "Find out how little time's left until upcoming Yale events"
    events = [
        Event("Bulldog Days", datetime.datetime(year=2019, month=4, day=15, hour=14)),
        Event("FSY", datetime.datetime(year=2019, month=6, day=25, hour=17)),
        Event("housing announcements", datetime.datetime(year=2019, month=6, day=26, hour=12)),
        Event("pre-orientation", datetime.datetime(year=2019, month=8, day=17, hour=12)),
        Event("orientation", datetime.datetime(year=2019, month=8, day=20)),
    ]

    def get_event(self, name):
        for option in self.events:
            if option.name == name:
                return option
        return None

    def response(self, query, message):
        if query:
            event = self.get_event(query)
            if event is None:
                return "Couldn't find the event '%s'" % query
            return str(event)
        events = self.remaining_events()
        if len(events) == 0:
            return "No upcoming events."
        return "\n".join([str(event) for event in events])

    def next_event(self) -> Event:
        """
        :return: next event in list.
        """
        now = datetime.datetime.now()
        for event in self.events:
            if (event.date - now).total_seconds() > 0:
                return event
        return None

    def remaining_events(self):
        now = datetime.datetime.now()
        for event in self.events:
            if (event.date - now).total_seconds() < 0:
                self.events.pop(0)
        return self.events
