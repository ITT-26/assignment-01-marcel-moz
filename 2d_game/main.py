import WindowHandler, pyglet, random
from pyglet import window
from DIPPID import SensorUDP
from GameObjectFactory import GameObjectFactory
from InputHandler import InputHandler


PORT = 5700
win = window.Window()
sensor = SensorUDP(PORT)

batch = pyglet.graphics.Batch()  # Batch for better draw performence
rockGroup = pyglet.graphics.Group(order=1)

factory = GameObjectFactory(win, batch)

input = InputHandler(win, sensor)

WindowHandler.setupWindow(win)


WIN_SECTION = win.width // 12
WIN_HEIGHT = win.height

backgroundSprite1, backgroundSprite2 = factory.createBackgroundSprites()
boat = factory.createBoat(5.5 * WIN_SECTION, 50, WIN_SECTION, 400)


@win.event
def on_draw():
    win.clear()
    batch.draw()


@win.event
def on_close():
    sensor.disconnect()
    pyglet.app.exit()


isPaused = False
isStarted = False
time = 0
rocks = []
lastRockSpawn = -2  # -2for 1st spawn after one second when time is 1 (game start t = 0)


def update(dt):
    global isPaused
    global isStarted
    global time
    global lastRockSpawn

    input.checkButton1ForClick()
    if input.checkButton1ForRelease():
        if not isStarted:
            isStarted = True  # wenn noch nicht gestartet bei Button release starten
            print("Start")
            return

        if isPaused and isStarted:
            isPaused = False
            print("Resume")

        elif not isPaused and isStarted:
            isPaused = True
            print("Pause")
            return

    if not isPaused and isStarted:
        time += dt

        spawn_interval = 2.5 * (random.random() + 1)
        print(spawn_interval)

        if time >= lastRockSpawn + spawn_interval:
            for i in range(2):
                rock = factory.generateRock(rockGroup)
                lastRockSpawn = time
                rocks.append(rock)
            
        if backgroundSprite1.y < -1 * WIN_HEIGHT:  # reset when image reaches end
            backgroundSprite1.y = backgroundSprite2.y + backgroundSprite2.height
        elif backgroundSprite2.y < -1 * WIN_HEIGHT:
            backgroundSprite2.y = backgroundSprite1.y + backgroundSprite1.height

        PIXEL_PER_SEC = win.height // 8

        backgroundSprite1.y -= PIXEL_PER_SEC * dt
        backgroundSprite2.y -= PIXEL_PER_SEC * dt

        for rock in rocks:
            rock.y -= PIXEL_PER_SEC * dt

            if (rock.y + rock.height) < 0:  # clear rocks that have passed the screen
                rocks.remove(rock)

        if sensor.has_capability("gravity"):
            boat.y += dt * (sensor.get_value("gravity")["z"] - 3) * 100
            boat.x += dt * sensor.get_value("gravity")["x"] * -100
            # boat.rotation = dt * sensor.get_value("gravity")["x"] * 50 / 360


pyglet.clock.schedule_interval(update, 0.02)  # 50 fps

pyglet.app.run()
