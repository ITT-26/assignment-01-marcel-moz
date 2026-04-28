import pyglet, sys
from pyglet import window
from pyglet.window import key
from DIPPID import SensorUDP


class InputHandler:

    def __init__(self, window, sensor):
        self.window = window
        self.sensor = sensor
        self.lastButtonStates = {'button_1' : 0, 'button_2' : 0, 'button_3': 0, 'button_4' : 0}

    def checkButtonForClick(self, buttonName):

        if self.sensor.has_capability(buttonName):
            lastButtonState = self.lastButtonStates[buttonName]
            if ( lastButtonState == 0) and self.sensor.get_value(buttonName) == 1:
                self.lastButtonStates[buttonName] = 1
                return True
        return False  # if no button with that name

    def checkButtonForRelease(self, buttonName):
        if self.sensor.has_capability(buttonName) and buttonName in self.lastButtonStates:
            lastButtonState = self.lastButtonStates[buttonName] 
            if (lastButtonState == 1) and self.sensor.get_value(buttonName) == 0:
                self.lastButtonStates[buttonName]  = 0
                return True
        return False  # if no button with that name

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.window.close()
            

    
    def getBoatInputAndMove(self,boat, dt):
        SPEED_FACTOR_X = 70
        SPEED_FACTOR_Y = 30
        new_x = boat.x + dt * self.sensor.get_value('gravity')['x'] * - SPEED_FACTOR_X
        new_y = boat.y + dt * (self.sensor.get_value('gravity')['z'] - 3) * SPEED_FACTOR_Y
        
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

    