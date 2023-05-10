from machine import Pin, PWM
from utils import *

def updateTemperature(currentTemp: int, newTemp: int, pin: Pin):

    #warmPin = PWM(Pin(15))
    coldPin = PWM(pin)

    print("Updating temperature")
    #warmPin.freq(1000)
    coldPin.freq(1000)

    if newTemp > currentTemp:
        print(f"We are at {currentTemp} and we want to go to {newTemp} getting colder")
        coldPin.duty_u16(65025)
    else:
        print(f"We are at {currentTemp} and we want to go to {newTemp} getting warmer")
        coldPin.duty_u16(0)
            

def loop(input_connection:socket.socket, controlPin: Pin, buffer):


    while True:

        # Receive new expected value
        newExpectedValue = ''
        try:
            newExpectedValue = int(input_connection.recv(1024))
            print("[Connection]:", f"Recieved new set-point: {newExpectedValue}")
            if newExpectedValue != "":
                (ambient_temp, box_temp) = buffer[-1]
                updateTemperature(ambient_temp,newExpectedValue,controlPin)
        except Exception:
            pass

def picoControlMainLoop(    picoIP:str,
                            input_port: int,
                            ambient_sensor_pin: int,
                            buffer:tuple[int,int]):

    # Start and setup input socket
    input_connection = open_socket(picoIP, input_port) # input requires pico IP
    print("Input socket started")
    input_connection.setblocking(False)

    # Pin
    controlPin = Pin(ambient_sensor_pin)

    # Main loop
    loop(input_connection, controlPin, buffer)