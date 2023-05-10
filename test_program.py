import network, socket, machine, onewire, ds18x20, time, utime

# Constants
ssid = 'virus'
password = 'joao1234'
server_ip = '192.168.172.108'
box_sensor_pin = 6 #GPIO number!
ambient_sensor = 999

# globals
buf = []

def connect(ssid_n, pwd_n):
    print("Starting connection")

    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid_n, pwd_n)

    # Waiting for Connection
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip, port):
    # Open a socket
    address = (ip, port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(address)
    print('[INFO]: connection to socket success')
    return connection

def get_temp_sensor(sensor_pin: int):
    # Start temperature sensor
    ds_pin = machine.Pin(sensor_pin)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    return ds_sensor, roms

def get_temp(sensor, roms):
    sensor.convert_temp()
    time.sleep_ms(750)
    
    # this will just return the first, yes
    for rom in roms:
        print("    [ROM]: Reading from rom: ", rom)
        return sensor.read_temp(rom)

def loop(connection, buffer, box_sensor):
    # Receive new expected value
    newExpectedValue = ''
    try:
        newExpectedValue = int(connection.recv(1024))
        print(newExpectedValue)
    except Exception:
        print("[ERROR]: could not recieve new setpoint from computer")
        pass
    
    # Start temperature sensor
    ds_pin = machine.Pin(box_sensor)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()

    # Get temperature
    print('[INFO]: getting box temp')
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    # _we NEED to wait about 750ms, the sensor takes time preparing the data_
    currentTemperature = ds_sensor.read_temp(roms[0])

    # Send to control center
    if newExpectedValue != '':
        print(f"new temperature of {newExpectedValue}")
        buffer.append((newExpectedValue,currentTemperature))
    
    # Prepare return data_
    now = utime.gmtime()
    #print(f"{now[3:6]} : {currentTemperature}")
    connection.send(f"{now[3:6]} : {currentTemperature}".encode())
    print("[INFO]: sent currentTemperature to computer")
    
def correct_loop(connection, box_sensor, buffer):
    # Receive new set-point
    new_expected_value = ''
    try:
        new_expected_value = int(connection.recv(1024))
        print("[INFO]: new_expected_value: ", new_expected_value)
    except Exception:
        print("[ERROR]: could not recieve new setpoint from computer")
        pass
    
    # Get temperature
    print('[INFO]: getting box temp')
    current_temp = get_temp(box_sensor)
    
    # Send to control center
    if new_expected_value != '':
        print("[INFO]: ", f"sent new temperature of {new_expected_value}")
        buffer.append((new_expected_value, current_temp))
    
    # Prepare return data_
    now = utime.gmtime()
    #print(f"{now[3:6]} : {currentTemperature}")
    connection.send(f"{now[3:6]} : {current_temp}".encode())
    print("[INFO]: sent current_temp to computer")
    pass

print(__name__)
print("starting test program")
connect(ssid, password)
con = open_socket(server_ip, 5000)
test_sensor = get_temp_sensor(box_sensor_pin)

while True:
    correct_loop(connection=con, box_sensor=test_sensor, buffer=buf)
    