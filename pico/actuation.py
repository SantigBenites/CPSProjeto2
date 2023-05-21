from machine import Pin, PWM
from time import sleep
from utils import *
from ctrl import PID


def picoControlMainLoop(pico_ip: str,
                        input_port: int,
                        fan_def: Control_Tuple,
                        res_def: Control_Tuple,
                        control_time: int,
                        buffer: list,
                        debug: bool):

    # Start and setup input socket
    input_connection = open_socket(pico_ip, input_port) # input requires pico IP
    print("Input socket started")
    input_connection.setblocking(False)

    # Set PWM pins for the fan and the resistor:
    fan_pwm = PWM(Pin(fan_def.pin))
    fan_pwm.freq(fan_def.freq)
    
    res_pwm = PWM(Pin(res_def.pin))
    res_pwm.freq(res_def.freq)

    fan_pid = PID('fan', fan_def.p, fan_def.i, fan_def.d, fan_def.min, fan_def.max, True)
    res_pid = PID('res', res_def.p, res_def.i, res_def.d, res_def.min, res_def.max, True)
    
    sleep(2)
    if debug:
        print('[DEBUG]:', 'Starting Control Main Loop...')
    # Main loop
    loop(input_connection, fan_pwm, res_pwm, fan_pid, res_pid, control_time, buffer, debug)


def loop(input_connection: socket.socket,
         fan_pwm: PWM,
         res_pwm: PWM,
         fan_pid: PID,
         res_pid: PID,
         control_time: int,
         buffer,
         debug: bool):
    
    set_point = 20
    chunk = 0
    
    while True:
        # Try to recieve the new set_point, if there is none, use the last set_point
        try:
            chunk = input_connection.recv(1024)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            else:
                set_point = int(chunk)
                print("[CONNECTION]:", f"Recieved new set-point: {set_point}")
        except Exception as e:
            print(e)
        
        if len(buffer) > 0:
            (ambient_temp, box_temp) = buffer.pop()
        else:
            (ambient_temp, box_temp) = (0,0)
        if debug: print('[DEBUG]:', f'will try to match box_temp -> {box_temp}, ambient_temp -> {ambient_temp} to set_point {set_point}')      
        
        update_temperature(ambient_temp, box_temp, set_point, fan_pwm, res_pwm, fan_pid, res_pid, debug)
        sleep(control_time)

        if(len(buffer) > 10):
            print('[DEBUG]:', f"buffer is going to be cleared {buffer}")  
            buffer.clear()
            print('[DEBUG]:', f"buffer was cleared {buffer}")  

def update_temperature(ambient_temp: float,
                      box_temp: float,
                      set_point: float,
                      fan_pwm: PWM,
                      res_pwm: PWM,
                      fan_pid: PID,
                      res_pid: PID,
                      debug: bool):

    fan_duty = fan_pid.update(set_point, box_temp)
    res_duty = res_pid.update(set_point, box_temp)

    if debug:
        print('[DEBUG]:', 'Updating Duty')
        print(f'    fan_duty -> {fan_duty}')
        print(f'    res_duty -> {res_duty}')

    fan_pwm.duty_u16(int(fan_duty))
    res_pwm.duty_u16(int(res_duty))
