from pid import PID
from time import sleep, time

controller = PID("resistor", 1, 1, 1, 0, 100, True)

for i in range(20):
    sleep(1)
    print('[CONTROLLER]:', controller.update(40, 0))