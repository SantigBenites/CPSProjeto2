import machine, onewire, ds18x20, time, utime

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

print('Found DS devs: ', roms)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)

    for rom in roms:
        # rom is byte array representing temp
        currentTemperature = ds_sensor.read_temp(rom)
        now = utime.gmtime()
        print(f"{now[3:6]} : {currentTemperature}")
    time.sleep(1.5)