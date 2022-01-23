from utime import sleep
from machine import Pin
from audio import playNotes
from state import IdleUIState
from display import initDisplay, updateDisplay


initDisplay()

incrButton = Pin(14, Pin.IN, Pin.PULL_DOWN)
enterButton = Pin(15, Pin.IN, Pin.PULL_DOWN)


def main():

    state = IdleUIState(None, True)
    updateDisplay(state.display())

    while True:
        incrPressed = incrButton.value()
        enterPressed = enterButton.value()
        if (incrPressed or enterPressed):
            if (incrPressed):
                state = state.incr()
            if (enterPressed):
                state = state.enter()
            updateDisplay(state.display())
            playNotes(state.notes)
            sleep(0.2)


main()
