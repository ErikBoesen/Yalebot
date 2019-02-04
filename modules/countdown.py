import datetime

BDD_TIME = datetime.datetime(year=2019, month=4, day=15)

class Countdown:
    def __init__(self):
        pass

    def response(self, query: str = None):
        """
        Calculate response given input.
        :param query: text input to command.
        """
        return 'There are %d weeks, %d days, %d hours, %d minutes, and %d seconds left until %s.' % (self.time())

    def time(self):
        """
        Get time split into units until Bulldog Days.
        """
        delta = BDD_TIME - datetime.datetime.now()
        seconds = delta.total_seconds()
        weeks, seconds = divmod(seconds, 60*60*24*7)
        days, seconds = divmod(seconds, 60*60*24)
        hours, seconds = divmod(seconds, 60*60)
        minutes, seconds = divmod(seconds, 60)
        return weeks, days, hours, minutes, seconds
