import network, socket, machine, onewire, ds18x20, time, utime, random
from utils import *

def get_temp_sensor(sensor_pin: int):
    # Start temperature sensor
    ds_pin = machine.Pin(sensor_pin)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print("[INFO]:", f"Created connection to temperature sensor in pin {sensor_pin}")
    return ds_sensor, roms

def get_temp(sensor, roms, sensor_type: str):
    """sensor_type should be either _box_ or _ambient_
    """
    sensor.convert_temp()
    time.sleep_ms(750)
    
    # this will just return the first, yes
    temperature = 0
    for rom in roms:
        temperature = sensor.read_temp(rom)
    print("[INFO]:", f"Reading temperature from {sensor_type} -> {temperature}")
    return temperature

def loop(output_connection:socket.socket, ambient_sensor, ambient_roms, box_sensor, box_roms, buffer):

    # Obtain data from ambient and box
    #box_temp = get_temp(box_sensor, box_roms, "box")
    box_temp = get_temp(box_sensor, box_roms, 'box')
    ambient_temp = get_temp(ambient_sensor, ambient_roms, 'ambient')
    
    # Update buffer data
    buffer.append((ambient_temp, box_temp))

    # Prepare return data
    now = utime.gmtime()
    currentTime = f"{now[3]}:{now[4]}:{now[5]}"
    output_connection.send(f"{currentTime} , {box_temp} \n".encode())

    

def picoConnectionMainLoop( picoIP:str,
                            output_port: int,
                            ambient_sensor_pin: int,
                            box_sensor_pin: int,
                            buffer):
    
    box_sensor, box_roms = get_temp_sensor(box_sensor_pin)
    ambient_sensor, ambient_roms = get_temp_sensor(ambient_sensor_pin)
    
    try:

        # Start and setup output socket
        output_connection = open_socket(picoIP, output_port) # output requires PC IP
        print("Output socket started")
        output_connection.setblocking(False)

        
        lastTime = time.time()
        while True:
            if time.time()  - lastTime > 1:
                lastTime = time.time()
                try:
                    loop(output_connection,
                         ambient_sensor,
                         ambient_roms,
                         box_sensor,
                         box_roms,
                         buffer)
                except Exception:
                    output_connection.close()  
    except KeyboardInterrupt:
        machine.reset()