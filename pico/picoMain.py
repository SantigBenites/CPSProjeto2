import _thread

from utils import *
from machine import Pin, PWM
from picoClient import picoConnectionMainLoop
from temperatureControl import picoControlMainLoop

import network, socket, machine, onewire, ds18x20, time, utime

# Constants
ssid = 'best_virus'
password = 'qwertyuiop'
server_ip = '192.168.185.108'
input_port = 5555
output_port = 4444
box_sensor_pin = 15 #GPIO number!
ambient_sensor_pin = 22

# PIN, FREQ, P, I, D
fan_def = Control_Tuple(0, 10000, 1, 1, 1)
res_def = Control_Tuple(0, 100000, 1, 1, 1)

# Connect pico to WLAN
picoIP = connect(ssid, password)
print("Waiting for PC connections")

# Inter-Thread communication buffer
bufferCurrentTemp = []

print("Thread Started")
_thread.start_new_thread(picoControlMainLoop, (picoIP, input_port, box_sensor_pin, bufferCurrentTemp))

picoConnectionMainLoop(picoIP, output_port, ambient_sensor_pin, box_sensor_pin, bufferCurrentTemp)

