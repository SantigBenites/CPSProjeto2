from ctrl import PID
from time import sleep, time
from machine import Pin, PWM


from utils import Control_Tuple

controller = PID("res", 1, 1, 1, 0, 100, True)


for i in range(40):
    sleep(2)
    print(f"iter {i}")
    print(controller.update(25, 21))

#res_pwm = PWM(Pin(16))
#res_pwm.freq(100000)
#res_pwm.duty_u16(0)

