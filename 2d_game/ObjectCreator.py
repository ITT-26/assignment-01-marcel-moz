import pyglet, random, math
from pyglet import shapes, image, sprite


class ObjectCreator:
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch

    def createBoat(self, x, y):
        RAFT_PATH = '.\\assets\\raft1.png'
        # Raft Sprite by Sevarihk https://opengameart.org/content/animated-pixel-art-raft-sprite
        raftImage = image.load(RAFT_PATH)
        boat = pyglet.sprite.Sprite(raftImage, x=x, y=y, batch=self.batch)

        aspect_ratio = boat.height / boat.width
        boat.width = self.window.width // 12
        boat.height = self.window.width // 12 * aspect_ratio

        return boat
    
    def setObjectPosition(self, object, x,y):
        object.x = x
        object.y = y

    def generateRock(self, group):
        ROCK_PATH = '.\\assets\\rock.png'
        ROCK_SIZE = self.window.height // 12

        x = math.floor(random.random() * self.window.width)
        y = self.window.height + (
            math.floor(random.random() * 5 * ROCK_SIZE)
        )  # litte bit of verstatz to break the pattern
        rockImage = image.load(ROCK_PATH)

        rock = pyglet.sprite.Sprite(rockImage, x=x, y=y, batch=self.batch, group=group)
        rock.width, rock.height = ROCK_SIZE, ROCK_SIZE
        return rock

    def createBackgroundSprites(self):
        BACKGROUND_IMAGE_PATH = '.\\assets\\ocean.png'

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

    def createBottomText(self, textGroup):
        bottom_text = pyglet.text.Label(
            'ESC / 4 = close game | 1 = pause / resume',
            font_name='Arial',
            font_size=36,
            x=20,
            y=20,
            anchor_x='left',
            anchor_y='bottom',
            batch=self.batch,
            group=textGroup,
            color=(255, 255, 255),
        ) 
        return bottom_text
    
    def createScoreText(self,textGroup):
        scoreText = pyglet.text.Label(
            '0',
            font_name='Arial',
            font_size=100,
            x=100,
            y=self.window.height - 100,
            anchor_x='left',
            anchor_y='top',
            batch=self.batch,
            group=textGroup,
            color=(255, 255, 255),
        ) 
        return scoreText
    
    def createCenterText(self,textGroup):
        centerText = pyglet.text.Label(
            'Press 1 to start the game',
            font_name='Arial',
            font_size=80,
            multiline=True,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch,
            group=textGroup,
            width=self.window.width//2.5,
            color=(255, 255, 255),
            align= 'center'
        ) 
        return centerText
