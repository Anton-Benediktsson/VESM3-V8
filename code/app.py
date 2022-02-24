# Þórhallur Tryggvason
# Get information from leap motion controller and sends it to mqtt server

import Leap     # See Python 3 section on leap motion controller
from time import sleep
import paho.mqtt.client as mqtt

#Constants
MAPSIZE = (-62, 62)     # Size of map should be (display-size / 2 - (playersize / 2)) in negative and positive
SERVER = "127.0.0.1"     # MQTT Server adress

#Clients
controller = Leap.Controller()
client = mqtt.Client()

#Functions
def pollController():      # Function to get palm position
    frame = controller.frame()
    hands = frame.hands
    rightmost_pos = hands.rightmost.palm_position
    leftmost_pos = hands.leftmost.palm_position
    return leftmost_pos[2],rightmost_pos[2]

def waitConnections():      # Function to connect to lmc and mqtt server
    while controller.is_connected is False:
        sleep(1)
    print("Controller Connected:", controller.is_connected)

    client.connect(SERVER)
    return


# Main Code
waitConnections()
while True:

    sleep(0.25)     # Amount of time between getting new information (info needs to be sent through mqtt)
    leftmost,rightmost = pollController()
    leftmost = round(leftmost)
    rightmost = round(rightmost)

    # If lmc does not detect any hands it will register 0 for both players sending the player to the middle being annoying for players
    # Following code will set position to old_pos if the sensor does not register anything
    # If running first old_pos does not exist so the code also needs to continue if error
    if leftmost == 0 and rightmost == 0:
        try:
            leftmost = old_pos[0]
            rightmost = old_pos[1]
        except:
            continue

    old_pos = [leftmost, rightmost]

    # Since there is no technically no limit to how far the sensor can detect your hands from you need to limit it to the size of the mapsize
    if leftmost < MAPSIZE[0]: leftmost = MAPSIZE[0]
    if leftmost > MAPSIZE[1]: leftmost = MAPSIZE[1]
    if rightmost < MAPSIZE[0]: rightmost = MAPSIZE[0]
    if rightmost > MAPSIZE[1]: rightmost = MAPSIZE[1]

    # Sends to mqtt server
    print(f"Leftmost: {leftmost}, Rightmost: {rightmost}")
    client.publish("game/players", f"{leftmost},{rightmost}")