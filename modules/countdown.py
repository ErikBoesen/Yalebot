import datetime


class Event:
    def __init__(self, name: str, date: datetime.datetime, duration: datetime.timedelta):
        self.name = name
        self.date = date
        self.duration = duration

class Countdown:
    events = [
        Event("Bulldog Days", datetime.datetime(year=2019, month=4, day=15), datetime.timedelta(days=3)),
    ]

    def __init__(self):
        pass

    def response(self, query: str = None):
        """
        Calculate response given input.
        :param query: text input to command.
        """
        return "There are %d weeks, %d days, %d hours, %d minutes, and %d seconds left until Bulldog Days." % (self.time())

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
        delta = event.date - now
        seconds = delta.total_seconds()
        weeks, seconds = divmod(seconds, 60*60*24*7)
        days, seconds = divmod(seconds, 60*60*24)
        hours, seconds = divmod(seconds, 60*60)
        minutes, seconds = divmod(seconds, 60)
        return weeks, days, hours, minutes, seconds
