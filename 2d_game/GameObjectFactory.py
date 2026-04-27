import pyglet, random, math
from pyglet import shapes, image, sprite


class GameObjectFactory:
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch

    def createBoat(self, x, y, width, height):
        boat = shapes.Rectangle(
            x, y, width, height, (0, 0, 0), batch=self.batch
        )  # hier statt übergabe parameter über window arbeiten
        return boat

    def generateRock(self,group):
        ROCK_SIZE  = self.window.height//18

        x =  math.floor(random.random() * self.window.width)
        y = self.window.height + (math.floor(random.random() * 4 * ROCK_SIZE)) # litte bit of verstatz to break the pattern
        
        rock = shapes.Rectangle(
            x, y, ROCK_SIZE , ROCK_SIZE, (0,0,0), batch=self.batch, group=group
        )
        return rock

    def createBackgroundSprites(self):
        BACKGROUND_IMAGE_PATH = ".\\assets\\ocean.png"

        backgroundImage = image.load(BACKGROUND_IMAGE_PATH)

        backgroundSprite1 = sprite.Sprite(
            backgroundImage, 0, 0, batch=self.batch
        )  # create sprite at correct position and in batch
        backgroundSprite1.height = self.window.height
        backgroundSprite1.width = self.window.width

        backgroundSprite2 = sprite.Sprite(
            backgroundImage, 0, backgroundSprite1.height, batch=self.batch
        )  # create sprite at correct position and in batch
        backgroundSprite2.height = self.window.height
        backgroundSprite2.width = self.window.width

        return [backgroundSprite1, backgroundSprite2]
