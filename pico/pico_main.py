import _thread

from utils import *
from machine import Pin, PWM
from sensor import picoConnectionMainLoop
from actuation import picoControlMainLoop

import network, socket, machine, onewire, ds18x20, time, utime

# Constants
ssid = 'best_virus'
password = 'qwertyuiop'
server_ip = '192.168.185.108'
input_port = 5555
output_port = 4444
box_sensor_pin = 20 #GPIO number!
ambient_sensor_pin = 18

# PIN, FREQ, P, I, D
fan_def = Control_Tuple(16, 100000, 300, 0.001, 40, 64700, 65535)
res_def = Control_Tuple(15, 5500, 1200, 0.015, 150, 0, 10000)
control_time = 3

# Connect pico to WLAN
picoIP = connect(ssid, password)
print("Waiting for PC connections")

# Inter-Thread communication buffer
bufferCurrentTemp = []


"""
(pico_ip: str,
input_port: int,
fan_def: Control_Tuple,
res_def: Control_Tuple,
control_time: int,
buffer: list,
debug: bool)
"""
print("Thread Started")
_thread.start_new_thread(picoControlMainLoop, (picoIP, input_port, fan_def, res_def, control_time, bufferCurrentTemp, True))

picoConnectionMainLoop(picoIP, output_port, ambient_sensor_pin, box_sensor_pin, bufferCurrentTemp)

