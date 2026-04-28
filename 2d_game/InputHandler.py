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

    def getBoatInputAndMove(self,boat, dt):
        SPEED_FACTOR = 70
        new_y = boat.y + dt * (self.sensor.get_value("gravity")["z"] - 3) * SPEED_FACTOR
        new_x = boat.x + dt * self.sensor.get_value("gravity")["x"] * - SPEED_FACTOR
        if new_y < 0:
            new_y = 0
        elif (new_y + boat.height) > self.window.height:
            new_y = self.window.height - boat.height
        if new_x < 0:
            new_x = 0
        elif (new_x + boat.width) > self.window.width:
            new_x = self.window.width - boat.width
        boat.y = new_y
        boat.x = new_x

    