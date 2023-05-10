import _thread
from picoClient import picoConnectionMainLoop
from temperatureControl import updateTemperature
from machine import Pin, PWM
from time import sleep
import network, socket, machine, onewire, ds18x20, time, utime

buffer = []

print("Thread Started")
#_thread.start_new_thread(updateTemperature, (buffer,))

picoConnectionMainLoop(buffer,"192.168.43.123",5000)


