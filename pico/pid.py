"""
PID class that implements the function:

duty(t) = K_p * e(t) + K_i * ∫ e(t) dt + K_d * (de(t)/dt)
"""
from time import time

class PID:

    cond = {
        'fan': lambda v: v < 0,
        'resistor': lambda v: v > 0
    }

    # name MUST be either fan or resistor
    def __init__(self,
                 name: str,
                 P: float,
                 I: float,
                 D: float,
                 controller_min: int,
                 controller_max: int,
                 debug: bool):
        
        # constants
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.name = name
        self.min = controller_min
        self.max = controller_max
        self.integral_values = [] # array that will store the 
        self.integral_number = 10 # max number of values for the roling window
        self.debug = debug
        
        # not...
        self.last_error = 0
        self.last_time = time()
        pass

    def update(self, set_point, process_variable):

        #get new time
        new_time = time()
        current_error = set_point - process_variable
        time_delta = new_time - self.last_time
        
        if self.debug:
            print(f'[DEBUG]: {self.name} PID controller')
            print(f'    time_delta -> {time_delta}')
            print(f'    current_error -> {current_error}')
            print(f'    last_time -> {self.last_time}')
            print(f'    new_time  -> {new_time}')

        # proportional
        p_val = self.Kp * current_error 

        # integral
        i_val = self.Ki * self.__integral(current_error, time_delta)

        # derivate
        d_val = self.Kd * ((current_error - self.last_error) / time_delta)

        # update:
        self.last_error = current_error
        self.last_time = new_time

        duty = p_val + i_val + d_val
        
        if self.debug:
            print(f'    p_val -> {p_val}')
            print(f'    i_val -> {i_val}')
            print(f'    d_val -> {d_val}')
            print(f'    duty  -> {duty}')

        return abs(duty) if self.cond[self.name](duty) else 0
    
    def __integral(self, error, dt):
        # Calculate the integral using the rectangle approximation
    
        if len(self.integral_values) >= self.integral_number:
            del self.integral_values[0]
            
        self.integral_values.append(error * dt)
        
        return sum(self.integral_values)