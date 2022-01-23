import audio


def getShortDateTime(date):
    return date[2] + '/' + date[1] + '/' + date[0] + ' ' + date[3] + ':' + date[4] + ':' + date[5]


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
        super(starterDate, fridgeIsOn)

    def incr(self):
        self.starterDate = self.starterDate[:2] + \
            (self.starterDate[2] + 1,) + self.starterDate[3:]
        return self

    def decr(self):
        self.starterDate = self.starterDate[:2] + \
            (self.starterDate[2] - 1,) + self.starterDate[3:]
        return self

    def enter(self):
        return SetEndTimeHHState(self.starterDate, self.fridgeIsOn)

    def display(self):
        return 'Set day: ' + self.starterDate[2]


class SetEndTimeHHState(BaseState):
    def __init__(self, starterDate, fridgeIsOn):
        super(starterDate, fridgeIsOn)

    def display(self):
        return 'Set hour: ' + self.starterDate[3]

    def incr(self):
        self.starterDate = self.starterDate[:3] + \
            (self.starterDate[3] + 1,) + self.starterDate[4:]
        return self

    def decr(self):
        self.starterDate = self.starterDate[:3] + \
            (self.starterDate[3] - 1,) + self.starterDate[4:]
        return self

    def enter(self):
        return IdleUIState(self.starterDate, self.fridgeIsOn)
