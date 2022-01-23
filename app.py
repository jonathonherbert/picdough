from utime import sleep, sleep_us, sleep_ms
from machine import Pin
from audio import playNotes, confirm, shift
from state import IdleUIState

rs = Pin(16, Pin.OUT)
e = Pin(17, Pin.OUT)
d4 = Pin(18, Pin.OUT)
d5 = Pin(19, Pin.OUT)
d6 = Pin(20, Pin.OUT)
d7 = Pin(21, Pin.OUT)
button1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(15, Pin.IN, Pin.PULL_DOWN)


def pulseE():
    e.value(1)
    sleep_us(40)
    e.value(0)
    sleep_us(40)


def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >> 0)
    d5.value((BinNum & 0b00000010) >> 1)
    d6.value((BinNum & 0b00000100) >> 2)
    d7.value((BinNum & 0b00001000) >> 3)
    pulseE()


def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >> 4)
    d5.value((BinNum & 0b00100000) >> 5)
    d6.value((BinNum & 0b01000000) >> 6)
    d7.value((BinNum & 0b10000000) >> 7)
    pulseE()
    d4.value((BinNum & 0b00000001) >> 0)
    d5.value((BinNum & 0b00000010) >> 1)
    d6.value((BinNum & 0b00000100) >> 2)
    d7.value((BinNum & 0b00001000) >> 3)
    pulseE()


def clearScreen():
    rs.value(0)
    send2LCD8(0b00000001)  # clear screen
    sleep_ms(2)  # clear screen needs a long delay
    rs.value(1)


def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)  # 8 bit
    send2LCD4(0b0011)  # 8 bit
    send2LCD4(0b0011)  # 8 bit
    send2LCD4(0b0010)  # 4 bit
    send2LCD8(0b00101000)  # 4 bit,2 lines?,5*8 bots
    send2LCD8(0b00001100)  # lcd on, blink off, cursor off.
    send2LCD8(0b00000110)  # increment cursor, no display shift
    send2LCD8(0b00000001)  # clear screen
    sleep_ms(2)  # clear screen needs a long delay
    rs.value(1)


setUpLCD()


def main():
    cursor = 0

    def updateDisplay(message):
        print("Display: " + message)
        clearScreen()
        for x in message:
            send2LCD8(ord(x))

    state = IdleUIState(None, True)

    while True:
        incrPressed = button1.value()
        enterPressed = button2.value()
        if (incrPressed or enterPressed):
            if (incrPressed):
                state = state.incr()
            if (enterPressed):
                state = state.enter()
            updateDisplay(state.display())
            playNotes(state.notes)
            sleep(0.2)


main()
