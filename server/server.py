import socket, time, random

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

def connect_to_remote_socket(ip:str,port:int):

    # Open a socket
    address = (ip, port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(address)
    connection.setblocking(False)
    return connection


def server_main_loop():
    
    picoIP = "192.168.43.76"
    picoInputSocket = 5555
    picoOutputSocket = 4444
    # Connect to input
    inputSocket = connect_to_remote_socket(picoIP,picoInputSocket)

    # Connect to Output
    outputSocket = connect_to_remote_socket(picoIP,picoOutputSocket)

    lastTime = time.time()
    try:
        while True:
            
            if time.time()  - lastTime > 5:
                lastTime = time.time()
                newTemp = random.randrange(20,30)
                print(f"Updating temp to {newTemp}")
                inputSocket.send(str(newTemp).encode('utf8'))

            try:
                data = outputSocket.recv(1024).decode()  # receive response
                print('Received from client: ' + data)  # show in terminal
                time.sleep(1)
            except Exception:
                pass
            

    except KeyboardInterrupt:

        print("Finished properly")
        inputSocket.close()
        outputSocket.close()

if __name__ == '__main__':
    server_main_loop()
