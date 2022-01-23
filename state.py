import audio
from utime import gmtime, mktime, localtime


def getShortDateTime(date):
    return '{}/{}/{} {}:{}:{}'.format(date[2], date[1], date[0], date[3], date[4], date[5])


class BaseState:
    notes = audio.shift

    def __init__(self, starterDate, fridgeIsOn):
        self.starterDate = starterDate
        self.fridgeIsOn = fridgeIsOn

    def noop(self):
        return self

    def incr(self):
        return self.noop()

    def decr(self):
        return self.noop()

    def enter(self):
        return self.noop()

    def display(self):
        pass


class IdleUIState(BaseState):
    notes = audio.confirm

    def enter(self):
        return SetEndTimeDDState(self.starterDate, self.fridgeIsOn)

    def display(self):
        return getShortDateTime(self.starterDate) if self.starterDate else 'No date set'


class SetEndTimeDDState(BaseState):
    def __init__(self, starterDate, fridgeIsOn):
        if (starterDate):
            super().__init__(starterDate, fridgeIsOn)
        else:
            now = gmtime()
            oneDayAhead = localtime(mktime((
                now[0], now[1], now[2] + 1, now[3], now[4], now[5], 0, 0)))
            super().__init__(oneDayAhead, fridgeIsOn)

    def incr(self):
        date = self.starterDate
        self.starterDate = localtime(mktime((
            date[0], date[1], date[2] + 1, date[3], date[4], date[5], date[6], date[7])))
        return self

    def decr(self):
        date = self.starterDate
        self.starterDate = localtime(mktime((
            date[0], date[1], date[2] - 1, date[3], date[4], date[5], date[6], date[7])))
        return self

    def enter(self):
        return SetEndTimeHHState(self.starterDate, self.fridgeIsOn)

    def display(self):
        return 'Set day: {}'.format(self.starterDate[2])


class SetEndTimeHHState(BaseState):
    def __init__(self, starterDate, fridgeIsOn):
        super().__init__(starterDate, fridgeIsOn)

    def display(self):
        return 'Set hour: {}'.format(self.starterDate[3])

    def incr(self):
        date = self.starterDate
        self.starterDate = localtime(mktime((
            date[0], date[1], date[2], date[3] + 1, date[4], date[5], date[6], date[7])))
        return self

    def decr(self):
        date = self.starterDate
        self.starterDate = localtime(mktime((
            date[0], date[1], date[2], date[3] + 1, date[4], date[5], date[6], date[7])))
        return self

    def enter(self):
        return IdleUIState(self.starterDate, self.fridgeIsOn)
