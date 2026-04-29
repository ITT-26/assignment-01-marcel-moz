class Game:
    def __init__(self):
        self.isPaused = False
        self.isStarted = False
        self.hasEnded = False
        self.time = 0
        self.rocks = []
        self.lastRockSpawn = (
            -2
        )  # -2for 1st spawn after one second when time is 1 (game start t = 0)
        self.score = 0

    def start(self):
        self.isStarted = True

    def pause(self):
        self.isPaused = True

    def resume(self):
        self.isPaused = False

    def end(self):
        self.hasEnded = True
        # for rock in self.rocks:
        #    rock.delete()
        # self.rocks.clear()

    def addTime(self, dt):
        self.time += dt

    def addScore(self, score):
        self.score += score

    def addRock(self, rock):
        self.rocks.append(rock)

    def removeRock(self, rock):
        self.rocks.remove(rock)

    

    def checkForBoatCollision(self, boat, object2):
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
