import WindowHandling
from pyglet import window, shapes, image, sprite
import pyglet
from DIPPID import SensorUDP
import time

win = window.Window()

PORT = 5700
sensor = SensorUDP(PORT)

WindowHandling.setWindowSizeMax(win)
WindowHandling.maximizeWindow(win)



BACKGROUND_IMAGE_PATH = '.\\assets\\ocean.png'
WIN_SECTION = win.width//12
WIN_HEIGHT = win.height

batch = pyglet.graphics.Batch() # Batch for better draw performence

backgroundImage = image.load(BACKGROUND_IMAGE_PATH)
backgroundSprite = sprite.Sprite(backgroundImage, 0, 0, batch=batch) #create sprite at correct position and in batch
backgroundSprite.height = WIN_HEIGHT 
backgroundSprite.width =  win.width 

backgroundSprite2 = sprite.Sprite(backgroundImage, 0, backgroundSprite.height, batch=batch) #create sprite at correct position and in batch
backgroundSprite2.height = WIN_HEIGHT 
backgroundSprite2.width =  win.width 

boat = shapes.Rectangle(5.5*WIN_SECTION, 50, WIN_SECTION, 400, (0,0,0), batch=batch)

lastButtonState = 0

def checkButtonForClick():
    global lastButtonState
    
    if sensor.has_capability('button_1'):    
        if (lastButtonState == 0) and sensor.get_value('button_1') == 1:
            lastButtonState = 1
            return True
    return False # if no button_1

def checkButtonForRelease():
    global lastButtonState 

    if sensor.has_capability('button_1'):
       if (lastButtonState == 1) and sensor.get_value('button_1') == 0:
           lastButtonState = 0
           return True
    return False # if no button_1

@win.event
def on_draw():
    win.clear()
    batch.draw()
    
isPaused = False

def update(dt):
    global isPaused
    global lastButtonState

    checkButtonForClick()
    if checkButtonForRelease():
        if isPaused:
            isPaused = False
            print("Resume")
        else:
            isPaused = True
            print("Pause")
            return
            
    
    if not isPaused: 
        if backgroundSprite.y < -1 * WIN_HEIGHT: #reset when image reaches end
            backgroundSprite.y = backgroundSprite2.y +  backgroundSprite2.height
        elif backgroundSprite2.y < - 1* WIN_HEIGHT:
            backgroundSprite2.y = backgroundSprite.y +  backgroundSprite.height

        backgroundSprite.y -= 500*dt
        backgroundSprite2.y -= 500*dt

        if sensor.has_capability('gravity'):
            boat.y += dt * (sensor.get_value('gravity')['z']-3) * 50
            boat.x += dt * sensor.get_value('gravity')['x'] * -50 
            boat.rotation =  dt * sensor.get_value('gravity')['x'] * 50 / 360

pyglet.clock.schedule_interval(update, 0.016) # 60 fps

pyglet.app.run()
