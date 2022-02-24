import Leap
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

    sleep(0.25)
    leftmost,rightmost = pollController()
    leftmost = round(leftmost)
    rightmost = round(rightmost)

    if leftmost == 0 and rightmost == 0:
        try:
            leftmost = old_pos[0]
            rightmost = old_pos[1]
        except:
            continue

    old_pos = [leftmost, rightmost]

    if leftmost < MAPSIZE[0]: leftmost = MAPSIZE[0]
    if leftmost > MAPSIZE[1]: leftmost = MAPSIZE[1]
    if rightmost < MAPSIZE[0]: rightmost = MAPSIZE[0]
    if rightmost > MAPSIZE[1]: rightmost = MAPSIZE[1]

    print(f"Leftmost: {leftmost}, Rightmost: {rightmost}")
    client.publish("game/players", f"{leftmost},{rightmost}")
