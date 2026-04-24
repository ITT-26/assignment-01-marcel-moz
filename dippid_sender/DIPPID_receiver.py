from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_accelerometer(data):
    print(data)

def handle_button_1(data):
    if int(data) == 0:
        print("Button 1 released")
    else:
        print("Button 1 pressed")

sensor.register_callback('button_1', handle_button_1)
sensor.register_callback('accelerometer', handle_accelerometer)

print("Receiver started and ready to go")
