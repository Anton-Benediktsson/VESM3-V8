import paho.mqtt.client as mqtt
import time
import os
from random import randrange
from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.pixel_mapper_config = "U-mapper;Rotate:270"
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options=options)

SERVER = "10.11.46.7" # IP for mqtt server

MAP_WIDTH = 128
MAP_HEIGHT = 128
PLAYER_WIDTH = 2
PLAYER_HEIGHT = 16
BALL_SPEED = round(MAP_WIDTH / 8)
WHITE = (255, 255, 255)

class Player():

    def __init__(self, position):
        self.center_x = position
        self.center_y = MAP_HEIGHT / 2
        self.score = 0

    def draw(self, draw):
        draw.rectangle([self.center_x + PLAYER_WIDTH / 2, self.center_y + PLAYER_HEIGHT / 2, self.center_x - PLAYER_WIDTH / 2, self.center_y - PLAYER_HEIGHT / 2], WHITE)

class Ball():

    def __init__(self):
        self.reset()
    
    def reset(self):

        self.center_x = MAP_WIDTH / 2
        self.center_y = MAP_HEIGHT / 2

        self.change_x = round(BALL_SPEED * randrange(-1, 2, 2) / randrange(2, 5))
        self.change_y = round((BALL_SPEED / 2) * randrange(-1, 2, 2) / randrange(2, 4))

    def on_update(self):

        if self.center_y >= MAP_HEIGHT or self.center_y <= 0:
            self.change_y = -self.change_y
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self, draw):
        draw.rectangle([self.center_x + MAP_WIDTH / 64, self.center_y + MAP_HEIGHT / 64, self.center_x - MAP_WIDTH / 64, self.center_y - MAP_HEIGHT / 64], WHITE)

class Main():

    def __init__(self):

        self.player_0 = Player(0 + PLAYER_WIDTH / 2)
        self.player_1 = Player(MAP_WIDTH - PLAYER_WIDTH / 2 - 1)
        self.ball = Ball()

        self.updateTime = 0
        self.scoreText = f"{self.player_0.score} - {self.player_1.score}"

        self.mqttSetup()
        self.update_setup()

    def mqttSetup(self):
        self.client = mqtt.Client()
        self.client.connect(SERVER)
        self.client.loop_start()
        self.client.subscribe("game/players")
        self.client.on_message = self.on_newPos

    def update_setup(self):

        start_time = time.time()

        while True:
            current_time = time.time()
            if current_time - start_time > 0.1:

                self.ball.on_update()
                self.render()
                self.on_update()
                start_time = time.time()

    def on_update(self):

        if self.ball.center_x <= self.player_0.center_x and self.ball.change_x < 0:
            if self.ball.center_y == self.player_0.center_y:
                self.ball.change_x = -self.ball.change_x
                self.ball.change_y = -self.ball.change_y
            elif self.ball.center_y < self.player_0.center_y and self.ball.center_y >= self.player_0.center_y - PLAYER_HEIGHT / 2 or self.ball.center_y > self.player_0.center_y and self.ball.center_y <= self.player_0.center_y + PLAYER_HEIGHT / 2:
                self.ball.change_x = -self.ball.change_y
                self.ball.change_y = -self.ball.change_x
            else:
                # add score for player 1
                self.player_1.score += 1
                self.ball.reset()
                self.scoreText = f"{self.player_0.score} - {self.player_1.score}"
        elif self.ball.center_x >= self.player_1.center_x and self.ball.change_x > 0:
            if self.ball.center_y == self.player_1.center_y:
                self.ball.change_x = -self.ball.change_x
                self.ball.change_y = -self.ball.change_y
            elif self.ball.center_y < self.player_1.center_y and self.ball.center_y >= self.player_1.center_y - PLAYER_HEIGHT / 2 or self.ball.center_y > self.player_1.center_y and self.ball.center_y <= self.player_1.center_y + PLAYER_HEIGHT / 2:
                self.ball.change_x = -self.ball.change_y
                self.ball.change_y = -self.ball.change_x
            else:
                #add score for player 0
                self.player_0.score += 1
                self.ball.reset()
                self.scoreText = f"{self.player_0.score} - {self.player_1.score}"

    def render(self):

        image = Image.new(mode="RGB" ,size=(MAP_WIDTH,MAP_HEIGHT))
        draw = ImageDraw.Draw(image)
        self.player_0.draw(draw)
        self.player_1.draw(draw)
        self.ball.draw(draw)
        draw.text((round(MAP_WIDTH / 2.5 - 1), MAP_HEIGHT - MAP_HEIGHT / 8), self.scoreText, WHITE)
        #print("Saving image")
        #image.save("/home/pi/app/image.png", "PNG")
        matrix.SetImage(image)

    def on_newPos(self, client, userdata, message):
        print(message)
        stuff = message.payload.decode()
        p0,p1 = map(int, stuff.split(","))
        p0 += MAP_HEIGHT / 2
        p1 += MAP_HEIGHT / 2
        print(p0, p1)
        self.player_0.center_y = p0
        self.player_1.center_y = p1

def main():
    try:

        Main()

    finally:
        pass
        #client.loop_stop()

main()
