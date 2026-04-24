import socket
import time
import json
import math
import random
import sys


IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def simulateAccData( t , freq):
    AMPLITUDE = 2 # Amplitude to allow higher Values (-2, 2)
    value = AMPLITUDE * math.sin(2*math.pi * freq * t) #2* math.pi for radian conversion
    return round(value, 8) # round value to match (roughly) the accuracy of DIPPID app

def sendMessage(key,value):  # function for sending either accelerometer or button message (usable for both)
    message_dict = {str(key): str(value)}
    message = json.dumps(message_dict)
    sock.sendto(message.encode(), (IP, PORT))
    
t = 0 # track runtime
DT = 0.1 # delta time for sleep time in each iteration
button_value = 0 # track button state

while True:
    try: 
        # calculate simulated accelerometer values for all axis
        # different freqeuncies for different values; odd freq for "odd" values (and avoid 0); dependent on t for changing values
        x = simulateAccData(t, 5.6) 
        y = simulateAccData(t, 9.3)
        z = simulateAccData(t, 2.1)

        sendMessage("accelerometer", [x,y,z]) # send acc mesage with calculated values

        if button_value == 1: # check if button was clicked in last iteration and release if so
            button_value = 0
            sendMessage("button_1", button_value)

    
        elif button_value == 0 and random.random()<= 0.1: # if button was not clicked last iteration determine click with randomizer
            button_value = 1                              # 10% chance for click
            sendMessage("button_1", button_value)

        t += DT   # update time variable to keep track
        time.sleep(DT) # sleep for delta t 

    except KeyboardInterrupt:
        print('Sender stopped') # short Interrupt msg for clean console
        sys.exit()
        

   
    

