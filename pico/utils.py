import socket, network, time

from collections import namedtuple

Control_Tuple = namedtuple("Control_Tuple", ["pin", "freq", "p", "i", "d"])


def connect(ssid, password):
    print("[INFO]:", "Starting connection")
    # Connect to WLAN
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
    input_socket = socket.socket()
    input_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    input_socket.bind(address)
    input_socket.listen(1)
    connection = input_socket.accept()[0]
    return connection


def clamp(value, min, max):
    if value > max: return max
    if value < min: return min
    return value