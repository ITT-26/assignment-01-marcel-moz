import WindowHandler, pyglet, random
from pyglet import window
from DIPPID import SensorUDP
from GameObjectFactory import GameObjectFactory
from InputHandler import InputHandler
from GameState import GameState


PORT = 5700
win = window.Window()
sensor = SensorUDP(PORT)

batch = pyglet.graphics.Batch()  # Batch for better draw performence
foreground = pyglet.graphics.Group(order=1)
textGroup = pyglet.graphics.Group(order=2)

factory = GameObjectFactory(win, batch)

input = InputHandler(win, sensor)


WindowHandler.setupWindow(win)


WIN_SECTION = win.width // 12
WIN_HEIGHT = win.height
WIN_WIDTH = win.width

backgroundSprite1, backgroundSprite2 = factory.createBackgroundSprites()
boat = factory.createBoat(5.5 * WIN_SECTION, 50)


centerText = pyglet.text.Label(
    "Press Button 1 to start",
    font_name="Felix Titling",
    font_size=80,
    x=win.width // 2,
    y=win.height // 2,
    anchor_x="center",
    anchor_y="center",
    batch=batch,
    group=textGroup,
    color=(255, 255, 255),
) # text am besten auch in game State
scoreText = pyglet.text.Label(
    "0",
    font_name="Felix Titling",
    font_size=100,
    x=100,
    y=win.height - 100,
    anchor_x="left",
    anchor_y="top",
    batch=batch,
    group=textGroup,
    color=(255, 255, 255),
) # textauch  game state


@win.event
def on_draw():
    win.clear()
    batch.draw()


@win.event
def on_close():
    sensor.disconnect()
    pyglet.app.exit()


def checkForCollision(object1, object2):
    seperated_x_1 = (
        object1.x > object2.x + object2.width
    )  # object 1 left side and object 2 right side
    seperated_x_2 = (
        object2.x > object1.x + object1.width
    )  # object 2 left side and object 1 right side
    seperated_y_1 = (
        object1.y > object2.y + object2.height
    )  # object 1 bottom object 2 bottom
    seperated_y_2 = (
        object2.y > object1.y + object1.height
    )  # object 1 bottom object 2 bottom

    if seperated_x_1 or seperated_x_2 or seperated_y_1 or seperated_y_2: #if seperated in any direction then no collision
        return False
    else:
        return True


game = GameState()


def update(dt):

    game.score = int(scoreText.text)  # get score as int

    input.checkButton1ForClick()
    if input.checkButton1ForRelease():
        if not game.isStarted:
            game.start()  # wenn noch nicht gestartet bei Button release starten
            centerText.opacity = 0  # hide center text
            return

        if game.isPaused and game.isStarted:
            game.resume()
            centerText.opacity = 0  # hide center text

        elif not game.isPaused and game.isStarted:
            game.pause()
            centerText.text = "PAUSE"  # center text auf pause setzen
            centerText.opacity = 255  # center text show
            return

    if not game.isPaused and game.isStarted and not game.hasEnded:
        game.addTime(dt)
        game.addScore(1)
        spawn_interval = 2.5 * (random.random() + 1)

        if game.time >= game.lastRockSpawn + spawn_interval:
            for i in range(5):
                rock = factory.generateRock(foreground)
                game.lastRockSpawn = game.time
                game.addRock(rock)
                game.addScore(25) # score bonus per rock

        scoreText.text = str(game.score)  # set score to label

        if backgroundSprite1.y < -1 * WIN_HEIGHT:  # reset when image reaches end
            backgroundSprite1.y = backgroundSprite2.y + backgroundSprite2.height
        elif backgroundSprite2.y < -1 * WIN_HEIGHT:
            backgroundSprite2.y = backgroundSprite1.y + backgroundSprite1.height

        PIXEL_PER_SEC = win.height // 8

        backgroundSprite1.y -= PIXEL_PER_SEC * dt
        backgroundSprite2.y -= PIXEL_PER_SEC * dt

        for rock in game.rocks:
            if checkForCollision(boat, rock):
                game.end()

            rock.y -= PIXEL_PER_SEC * dt

            if (rock.y + rock.height) < 0:  # clear rocks that have passed the screen
                game.removeRock(rock)
                rock.delete() # delte rock to free space (remove from batch)

        if sensor.has_capability("gravity"):
            input.getBoatInputAndMove(boat, dt)
          


pyglet.clock.schedule_interval(update, 0.02)  # 50 fps

pyglet.app.run()
