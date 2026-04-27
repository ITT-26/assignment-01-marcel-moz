import pyglet
from pyglet import window, display


def setupWindow(window):
    setWindowSizeMax(window)
    window.maximize()
    window.set_caption("Super Cool Boat Game")


def setWindowSizeMax(window):
    display = pyglet.display.get_display()
    screen = display.get_default_screen()
    window.width = screen.width
    window.height = screen.height
