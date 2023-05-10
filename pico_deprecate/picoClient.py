import network, socket, machine, onewire, ds18x20, time, utime


def connect():
    
    # WLAN credentials
    ssid = 'best_virus'
    password = 'qwertyuiop'
    print("Starting connection")

    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Waiting for Connection
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip,port):
    # Open a socket
    address = (ip, port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(address)
    return connection

def loop(connection,buffer):

    # Receive new expected value
    newExpectedValue = ''
    try:
        newExpectedValue = int(connection.recv(1024))
        print(newExpectedValue)
    except Exception:
        pass
    

    # Start temperature sensor
    ds_pin = machine.Pin(22)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()

    # Get temperature
    ds_sensor.convert_temp()
    currentTemperature = ds_sensor.read_temp(roms[0])

    # Send to control center
    if newExpectedValue != '':
        print(f"new temperature of {newExpectedValue}")
        buffer.append((newExpectedValue,currentTemperature))
    
    # Prepare return data
    now = utime.gmtime()
    #print(f"{now[3:6]} : {currentTemperature}")
    connection.send(f"{now[3:6]} : {currentTemperature}".encode())
    

def picoConnectionMainLoop(buffer:list, serverIP:str, portIP:int):
    try:
        picoIP = connect()
        connection = open_socket(serverIP,portIP)
        connection.setblocking(0)
        lastTime = time.time()
        
        while True:

            if time.time()  - lastTime > 1:
                lastTime = time.time()
                try:
                    loop(connection,buffer)
                except Exception:
                    connection.close()
    except KeyboardInterrupt:
        machine.reset()