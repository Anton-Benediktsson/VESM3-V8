# Þórhallur Tryggvason
# Game code to be run on raspberry pi

import paho.mqtt.client as mqtt
import time
import os
from random import randrange
from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions       # See Led Matrix section in readme.md

# Use RGBMatrixOptions library to set options for rgbmatrix
options = RGBMatrixOptions()

# Sets size of display
options.rows = 64
options.cols = 64

# Sets amount of displays
options.chain_length = 4
options.parallel = 1        # On adafruit-hat you cannot have more than 1 parallel

# "U-mapper" setting is for using all displays as a singular display. "Rotate" turns the screen to be corrctly aligned
options.pixel_mapper_config = "U-mapper;Rotate:270"
options.hardware_mapping = 'adafruit-hat'

# Sets matrix client with options
matrix = RGBMatrix(options=options)

SERVER = "10.11.46.7" # IP for mqtt server

# Designating map size, player size, base ball speed and a constant with tuple for RGB white color
MAP_WIDTH = 128
MAP_HEIGHT = 128
PLAYER_WIDTH = 2
PLAYER_HEIGHT = 16
BALL_SPEED = round(MAP_WIDTH / 8)
WHITE = (255, 255, 255)

# Player class contains variables and draw function
class Player():

    # Set variables for x,y and score
    def __init__(self, position):
        self.center_x = position
        self.center_y = MAP_HEIGHT / 2
        self.score = 0

    # Function to draw player on pillow image
    def draw(self, draw):
        draw.rectangle([self.center_x + PLAYER_WIDTH / 2,
        self.center_y + PLAYER_HEIGHT / 2,
        self.center_x - PLAYER_WIDTH / 2,
        self.center_y - PLAYER_HEIGHT / 2],
        WHITE)

# Ball class to store variables, calculate ballspeed, reset ball, move ball and draw ball on pillow image
class Ball():

    def __init__(self):
        self.reset()
    
    # Function for to set the position variable and to calculate ball speed
    def reset(self):

        # Set to center screen
        self.center_x = MAP_WIDTH / 2
        self.center_y = MAP_HEIGHT / 2

        # calculation for random ballspeed
        self.change_x = round(BALL_SPEED * randrange(-1, 2, 2) / randrange(2, 5))
        self.change_y = round((BALL_SPEED / 2) * randrange(-1, 2, 2) / randrange(2, 4))

    # Function that runs every frame (0.1 seconds | 10 fps)
    def on_update(self):

        # Checks if ball is at map border and reverses ball if it is
        if self.center_y >= MAP_HEIGHT or self.center_y <= 0:
            self.change_y = -self.change_y

        # Adds ball speed to location to adjust position
        self.center_x += self.change_x
        self.center_y += self.change_y

    # Function to draw ball
    def draw(self, draw):
        draw.rectangle([self.center_x + MAP_WIDTH / 64,
        self.center_y + MAP_HEIGHT / 64,
        self.center_x - MAP_WIDTH / 64,
        self.center_y - MAP_HEIGHT / 64],
        WHITE)

# Main game class, contains all operations Player and Ball did not contain
class Main():

    def __init__(self):

        # Sets the player_0, player_1 and ball variables to their classes
        self.player_0 = Player(0 + PLAYER_WIDTH / 2)
        self.player_1 = Player(MAP_WIDTH - PLAYER_WIDTH / 2 - 1)
        self.ball = Ball()

        # Scoretext string to appear at bottom screen
        self.scoreText = f"{self.player_0.score} - {self.player_1.score}"

        # Triggers the mqttSetup function to start mqtt receiver and update_setup to create game time
        self.mqttSetup()
        self.update_setup()

    # Function to connect to mqtt server, start loop to check for new data and sends new data to on_newPos function
    def mqttSetup(self):
        self.client = mqtt.Client()
        self.client.connect(SERVER)
        self.client.loop_start()
        self.client.subscribe("game/players")
        self.client.on_message = self.on_newPos

    # The main loop function of the game
    def update_setup(self):

        start_time = time.time()

        while True:
            current_time = time.time()
            # Loop uses start_time - current_time > delay to execute functions
            if current_time - start_time > 0.1:     # Every (0.1 seconds | 10 fps)

                self.ball.on_update()   # Updates ball function
                self.render()       # Renders a new image to scren
                self.on_update()    # Triggers on_update function to check if ball is colliding with players or is passing through
                start_time = time.time()

    def on_update(self):

        # Executes if ball and player_0 has same x value and the ball still has speed
        if self.ball.center_x <= self.player_0.center_x and self.ball.change_x < 0:
            # If ball lands on center of player it will only inver the values
            if self.ball.center_y == self.player_0.center_y:
                self.ball.change_x = -self.ball.change_x
                self.ball.change_y = -self.ball.change_y

            # If ball lands on sides of players it will invert so y = -x and x = -y
            elif self.ball.center_y < self.player_0.center_y \
            and self.ball.center_y >= self.player_0.center_y - PLAYER_HEIGHT / 2 \
            or self.ball.center_y > self.player_0.center_y \
            and self.ball.center_y <= self.player_0.center_y + PLAYER_HEIGHT / 2:

                self.ball.change_x = -self.ball.change_y
                self.ball.change_y = -self.ball.change_x
            # If ball goes past player it will add score to player, reset the ball and update scoreboard
            else:
                # add score for player 1
                self.player_1.score += 1
                self.ball.reset()
                self.scoreText = f"{self.player_0.score} - {self.player_1.score}"

        # Does same thing as above code but for other player
        elif self.ball.center_x >= self.player_1.center_x and self.ball.change_x > 0:
            if self.ball.center_y == self.player_1.center_y:
                self.ball.change_x = -self.ball.change_x
                self.ball.change_y = -self.ball.change_y

            elif self.ball.center_y < self.player_1.center_y \
            and self.ball.center_y >= self.player_1.center_y - PLAYER_HEIGHT / 2 \
            or self.ball.center_y > self.player_1.center_y \
            and self.ball.center_y <= self.player_1.center_y + PLAYER_HEIGHT / 2:

                self.ball.change_x = -self.ball.change_y
                self.ball.change_y = -self.ball.change_x
            else:
                #add score for player 0
                self.player_0.score += 1
                self.ball.reset()
                self.scoreText = f"{self.player_0.score} - {self.player_1.score}"

    # Function to render image
    def render(self):

        # Creates a new image with mode RGB (matrix does not support single color)
        image = Image.new(mode="RGB" ,size=(MAP_WIDTH,MAP_HEIGHT))
        # Creates draw class and draws both players, ball and text
        draw = ImageDraw.Draw(image)
        self.player_0.draw(draw)
        self.player_1.draw(draw)
        self.ball.draw(draw)
        draw.text((round(MAP_WIDTH / 2.5 - 1), MAP_HEIGHT - MAP_HEIGHT / 8), self.scoreText, WHITE)

        # Sends image to led matrix
        #print("Saving image")
        #image.save("/home/pi/app/image.png", "PNG")
        matrix.SetImage(image)

    # Function if new information is available from mqtt server and sets the new positions
    def on_newPos(self, client, userdata, message):
        stuff = message.payload.decode()
        p0,p1 = map(int, stuff.split(","))
        p0 += MAP_HEIGHT / 2
        p1 += MAP_HEIGHT / 2
        print(p0, p1)
        self.player_0.center_y = p0
        self.player_1.center_y = p1

def main():
    Main()

main()