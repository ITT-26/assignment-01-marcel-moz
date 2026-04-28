

class Game:
    def __init__(self):
        self.isPaused = False
        self.isStarted = False
        self.hasEnded = False
        self.time = 0
        self.rocks = []
        self.lastRockSpawn = -2  # -2for 1st spawn after one second when time is 1 (game start t = 0)
        self.score = 0

    def start(self):
        self.isStarted = True 

    def pause(self):
        self.isPaused = True
    
    def resume(self):
        self.isPaused = False

    def end(self):
        self.hasEnded = True
        #for rock in self.rocks:
        #    rock.delete()
        #self.rocks.clear()

    def addTime(self, dt):
        self.time += dt
    
    def addScore(self, score):
        self.score += score
    
    def addRock(self, rock):
        self.rocks.append(rock)

    def removeRock(self, rock):
        self.rocks.remove(rock)
    
    