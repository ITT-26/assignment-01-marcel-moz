import WindowHandling, pyglet, random
from pyglet import window
from DIPPID import SensorUDP
from ObjectCreator import ObjectCreator
from InputHandler import InputHandler
from Game import Game

PORT = 5700
win = window.Window()
sensor = SensorUDP(PORT)

batch = pyglet.graphics.Batch()  # Batch for better draw performence
foreground = pyglet.graphics.Group(order=1)
textGroup = pyglet.graphics.Group(order=2)

objectCreator = ObjectCreator(win, batch)

input = InputHandler(win, sensor)


WindowHandling.setupWindow(win)


WIN_SECTION = win.width // 12
WIN_HEIGHT = win.height
WIN_WIDTH = win.width

backgroundSprite1, backgroundSprite2 = objectCreator.createBackgroundSprites()
boat = objectCreator.createBoat(5.5 * WIN_SECTION, 50)

centerText = objectCreator.createCenterText(textGroup)
bottomText = objectCreator.createBottomText(textGroup)
scoreText = objectCreator.createScoreText(textGroup)


@win.event
def on_draw():
    win.clear()
    batch.draw()


@win.event
def on_close():
    sensor.disconnect()
    pyglet.app.exit()

game = Game()


def update(dt):
    global game

    game.score = int(scoreText.text)  # get score set from last update as int

    input.checkButtonForClick("button_4")  # always check button 4 for close
    if input.checkButtonForRelease("button_4"):
        win.close()
        sensor.disconnect()
        pyglet.app.exit()  # idk why on_close does not work here

    if game.hasEnded:
        if centerText.opacity == 0:  # wenn noch kein text ausgeblendet
            centerText.text = (
                "Game Over\n"
                "You crashed...\n"
                "Your score is: {}\n"
                "Press 2 to restart".format(game.score)
            )  # center text auf end text setzen setzen
            centerText.opacity = 255  # center text show
            return
        input.checkButtonForClick("button_2")
        if input.checkButtonForRelease("button_2"):
            resetBoatPosition()
            game = Game()
            centerText.text = "Press 1 to start the game"
            scoreText.text = str(game.score)
    if not game.hasEnded:
        input.checkButtonForClick("button_1")
        if input.checkButtonForRelease("button_1"):
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
        game.addScore(1)  # add score per "dt" unit (0.02)
        spawn_interval = 2.5 * (
            random.random() + 1
        )  # litte bit of variance for spawn_interval to not have a visible pattern

        if game.time >= game.lastRockSpawn + spawn_interval:
            for i in range(5):  # 5 rocks for more difficulty
                rock = objectCreator.generateRock(foreground)
                game.lastRockSpawn = game.time
                game.addRock(rock)  # spawn rock
                game.addScore(25)  # score bonus per rock

        scoreText.text = str(game.score)  # set score to label

        if (
            backgroundSprite1.y < -1 * WIN_HEIGHT
        ):  # reset (set above window)  when sprite1 reaches end
            backgroundSprite1.y = backgroundSprite2.y + backgroundSprite2.height
        elif (
            backgroundSprite2.y < -1 * WIN_HEIGHT
        ):  # reset (set above window) when sprite2 reaches end
            backgroundSprite2.y = backgroundSprite1.y + backgroundSprite1.height

        PIXEL_PER_SEC = win.height // 8

        backgroundSprite1.y -= PIXEL_PER_SEC * dt  # move background
        backgroundSprite2.y -= PIXEL_PER_SEC * dt

        for rock in game.rocks:
            if checkForBoatCollision(boat, rock):
                game.end()
                return
            rock.y -= PIXEL_PER_SEC * dt  # move rocks at same speed as background
            if (rock.y + rock.height) < 0:  # clear rocks that have passed the screen
                game.removeRock(rock)
                rock.delete()  # delte rock to free space (remove from batch)

        input.getBoatInputAndMove(boat, dt)


pyglet.clock.schedule_interval(update, 0.02)  # 50 fps

pyglet.app.run()

def resetBoatPosition():
    boat.x = 5.5 * WIN_SECTION
    boat.y = 50



def checkForBoatCollision(boat, object2):
    seperated_x_1 = (
        boat.x + boat.width // 20
        > object2.x + object2.width  # + boat.widht//20 for grace area
    )  # object 1 left side further left than object 2 right side
    seperated_x_2 = (
        object2.x + boat.width // 20
        > boat.x + boat.width  # + boat.widht//20 for grace area
    )  # object 2 left side further left than object 1 right side
    seperated_y_1 = (
        boat.y + boat.height // 8
        > object2.y
        + object2.height  # + boat.height//8 for grace area (sail, white dots)
    )  # object 1 bottom above object 2 top
    seperated_y_2 = (
        object2.y + boat.height // 8
        > boat.y + boat.height  # +  boat.height//8 for grace area (sail, white dots)
    )  # object 2 bottom above object 1 top

    if (
        seperated_x_1 or seperated_x_2 or seperated_y_1 or seperated_y_2
    ):  # if seperated in any direction then no collision
        return False
    else:
        return True


