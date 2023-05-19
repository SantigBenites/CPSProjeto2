#quick stop
from machine import Pin, PWM

fan_pwm = PWM(Pin(16))
fan_pwm.freq(100000)
    
res_pwm = PWM(Pin(15))
res_pwm.freq(5500)


fan_pwm.duty_u16(0)
res_pwm.duty_u16(0)
