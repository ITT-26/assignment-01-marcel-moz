import pyglet
from pyglet import window, display



def setWindowSizeMax(window):
        display = pyglet.display.get_display()
        screen = display.get_default_screen()
        window.width = screen.width  
        window.height = screen.height  
    
def maximizeWindow(window):
        window.maximize()
      