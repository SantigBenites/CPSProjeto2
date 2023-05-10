import machine
from time import sleep

pinn = machine.Pin("LED", machine.Pin.OUT)

while True:
    pinn.toggle()
    sleep(1)