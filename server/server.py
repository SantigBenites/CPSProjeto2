import socket, time

ssid = 'best_virus'
password = 'qwertyuiop'

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def client_program():
    host = get_ip()  # as both code is running on same pc
    port = 5000  # socket server port number
    print(f"Server running at {host}:{port}")

    address = (host, port)
    connectionSocket = socket.socket()
    connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connectionSocket.bind(address)
    connectionSocket.listen(1)
    
    try:
        while True:
            clientSocket = connectionSocket.accept()[0]
            data = clientSocket.recv(1024).decode()  # receive response
            print('Received from client: ' + data)  # show in terminal
            time.sleep(1)
            clientSocket.close()

    except KeyboardInterrupt:

        print("Finished properly")
        connectionSocket.close()

if __name__ == '__main__':
    client_program()