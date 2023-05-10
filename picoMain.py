import _thread
from picoClient import picoConnectionMainLoop
from temperatureControl import updateTemperature
from machine import Pin, PWM
import network, socket, machine, onewire, ds18x20, time, utime

# Constants
ssid = 'virus'
password = 'joao1234'
server_ip = '192.168.185.108'
server_port = 5000
box_sensor_pin = 0 #GPIO number!
ambient_sensor_pin = 4

buffer = []

print("Thread Started")
_thread.start_new_thread(updateTemperature, (buffer,))

picoConnectionMainLoop(buffer, server_ip, server_port, ssid, password, box_sensor_pin, ambient_sensor_pin)
