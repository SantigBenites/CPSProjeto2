import network, socket, machine, onewire, ds18x20, time, utime

ssid = 'best_virus'
password = 'qwertyuiop'


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip,port):
    # Open a socket
    address = (ip, port)
    connection = socket.socket()
    connection.connect(address)
    return connection

def serve(connection):
    #Start a web server
    ds_pin = machine.Pin(22)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()

    ds_sensor.convert_temp()

    currentTemperature = ds_sensor.read_temp(roms[0])
    now = utime.gmtime()
    print(f"{now[3:6]} : {currentTemperature}")
    connection.send(f"{now[3:6]} : {currentTemperature}")

    #for rom in roms:
    #    currentTemperature = ds_sensor.read_temp(rom)
    #    now = utime.gmtime()
    #    print(f"{now[3:6]} : {currentTemperature}")
    #    connection.send(f"{now[3:6]} : {currentTemperature}")
    

try:
    ip = "192.168.43.123"
    port = 5000
    picoIP = connect()
    print("connecting")
    while True:
        connection = open_socket(ip,port)
        try:
            serve(connection)
            connection.close()
        except Exception:
            connection.close()
except KeyboardInterrupt:
    machine.reset()