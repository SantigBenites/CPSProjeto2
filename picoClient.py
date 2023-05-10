import network, socket, machine, onewire, ds18x20, time, utime

def connect(ssid, password):
    print("[INFO]:", "Starting connection")
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Waiting for Connection
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print("[INFO]:", f'Connected on {ip}')
    return ip

def open_socket(ip, port):
    # Open a socket
    address = (ip, port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(address)
    return connection

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
    for rom in roms:
        temperature = sensor.read_temp(rom)
    print("[INFO]:", f"Reading temperature from {sensor_type} -> {temperature}")
    return temperature

def loop(connection, buffer, box_sensor, box_roms, ambient_sensor, ambient_roms):

    # Receive new expected value
    newExpectedValue = ''
    try:
        newExpectedValue = int(connection.recv(1024))
        print("[Connection]:", f"Recieved new set-point: {newExpectedValue}")
    except Exception:
        pass
    
    box_temp = get_temp(box_sensor, box_roms, "box")
    ambient_temp = get_temp(ambient_sensor, ambient_roms, "ambient")

    # Send to control center
    if newExpectedValue != '':
        print(f"new temperature of {newExpectedValue}")
        buffer.append((newExpectedValue, box_temp))
    
    # Prepare return data
    now = utime.gmtime()
    #print(f"{now[3:6]} : {box_temp}")
    connection.send(f"{now[3:6]} : {box_temp}".encode())
    

def picoConnectionMainLoop(buffer: list,
                           server_ip: str,
                           server_port: int,
                           wlan_ssid: str,
                           wlan_password: str,
                           box_sensor_pin: int,
                           ambient_sensor_pin: int):
    
    box_sensor, box_roms = get_temp_sensor(box_sensor_pin)
    ambient_sensor, ambient_roms = get_temp_sensor(ambient_sensor_pin)
    
    try:
        picoIP = connect(wlan_ssid, wlan_password)
        connection = open_socket(server_ip, server_port)
        connection.setblocking(0)
        lastTime = time.time()
        while True:
            if time.time()  - lastTime > 1:
                lastTime = time.time()
                try:
                    loop(connection,
                         buffer,
                         box_sensor,
                         box_roms,
                         ambient_sensor,
                         ambient_roms)
                except Exception:
                    connection.close()
    except KeyboardInterrupt:
        machine.reset()