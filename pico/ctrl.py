from time import time
from utils import range_map

class PID:
    """
    PID class that implements the function:

    duty(t) = K_p * e(t) + K_i * ∫ e(t) dt + K_d * (de(t)/dt)
    """

    cond = {
        'fan': lambda v: v > 0,
        'res': lambda v: v < 0
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
        self.max_value = 5 #This can never be 0
        pass

    def update(self, set_point, process_variable):

        #get new time
        new_time = time()
        current_error = set_point - process_variable
        time_delta = new_time - self.last_time
        
        if self.debug:
            print(f'[DEBUG]: {self.name} PID controller')
            print(f'    last_time -> {self.last_time}')
            print(f'    new_time  -> {new_time}')
            print(f'    time_delta -> {time_delta}')
            print(f'    last_error -> {self.last_error}')
            print(f'    current_error -> {current_error}')

        # proportional
        p_val = self.Kp * current_error 

        # integral
        i_val = self.Ki * self.__integral(current_error, time_delta)

        # derivate
        d_val = self.Kd * ((current_error - self.last_error) / time_delta)

        pid_value = p_val + i_val + d_val

        # update:
        self.last_error = current_error
        self.last_time = new_time
        if pid_value > self.max_value:
            self.max_value = pid_value

        # finish early if the pid is not supposed to do anything
        if self.cond[self.name](pid_value):
            print(f'    pid_value  -> {pid_value}')
            print(f'    actuation  -> {0}')
            return 0

        duty = range_map(abs(pid_value), 0, self.max_value, self.min, self.max)
        
        if self.debug:
            print(f'    p_val -> {p_val}')
            print(f'    i_val -> {i_val}')
            print(f'    d_val -> {d_val}')
            print(f'    pid_value  -> {pid_value}')
            print(f'    res   -> {duty}')

        return duty
    
    def __integral(self, error, dt):
        # Calculate the integral using rectangle approximation
        # and a roling window of size self.integral_number 
    
        if len(self.integral_values) >= self.integral_number:
            del self.integral_values[0]
            
        self.integral_values.append(error * dt)
        
        return sum(self.integral_values)
