import _thread
from picoClient import picoConnectionMainLoop
from temperatureControl import updateTemperature
from machine import Pin, PWM
import network, socket, machine, onewire, ds18x20, time, utime

# Constants
ssid = 'best_virus'
password = 'qwertyuiop'
server_ip = '192.168.185.108'
input_port = 5555
output_port = 4444
box_sensor_pin = 15 #GPIO number!
ambient_sensor_pin = 22

buffer = []

print("Thread Started")
_thread.start_new_thread(updateTemperature, (buffer,))

picoConnectionMainLoop(buffer, server_ip, input_port, output_port, ssid, password, box_sensor_pin, ambient_sensor_pin)
