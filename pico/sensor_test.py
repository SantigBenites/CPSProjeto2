import network, socket, machine, onewire, ds18x20, time, utime, random

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

box, box_roms = get_temp_sensor(20)
out, out_roms = get_temp_sensor(18)

while True:
    utime.sleep(1)
    get_temp(box, box_roms, 'box')
    
    get_temp(out, out_roms, 'out')
    