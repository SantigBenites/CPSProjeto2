from machine import Pin, PWM
from time import sleep
from utils import *
from pid import PID


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

    fan_pid = PID('fan', fan_def.p, fan_def.i, fan_def.d, 0, 100, True)
    res_pid = PID('fan', res_def.p, res_def.i, res_def.d, 0, 100, True)

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
    while True:
        # Receive new expected value
        new_set_point = ''
        try:
            new_set_point = int(input_connection.recv(1024))
            print("[CONNECTION]:", f"Recieved new set-point: {new_set_point}")
            if new_set_point != "":
                (ambient_temp, box_temp) = buffer[-1]
                update_temperature(ambient_temp, new_set_point, fan_pwm, fan_pid, res_pwm, res_pid, debug)
                sleep(control_time)
        except Exception:
            pass


def update_temperature(ambient_temp: float,
                      box_temp: float,
                      set_point: float,
                      fan_pwm: PWM,
                      res_pwm: PWM,
                      fan_pid: PID,
                      res_pid: PID,
                      debug: bool):

    if debug:
        print('[DEBUG]:', 'Updating Temperature')

    fan_pwm.duty_u16(fan_pid.update(set_point, box_temp))
    res_pwm.duty_u16(res_pid.update(set_point, box_temp))
