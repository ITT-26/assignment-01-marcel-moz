import pyglet, sys
from pyglet import window
from pyglet.window import key
from DIPPID import SensorUDP


class InputHandler:

    def __init__(self, window, sensor):
        self.window = window
        self.sensor = sensor
        self.lastButton1State = 0

    def checkButton1ForClick(self):

        if self.sensor.has_capability("button_1"):
            if (self.lastButton1State == 0) and self.sensor.get_value("button_1") == 1:
                self.lastButton1State = 1
                return True
        return False  # if no button_1

    def checkButton1ForRelease(self):
        global lastButton1State

        if self.sensor.has_capability("button_1"):
            if (self.lastButton1State == 1) and self.sensor.get_value("button_1") == 0:
                self.lastButton1State = 0
                return True
        return False  # if no button_1

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.window.close()
