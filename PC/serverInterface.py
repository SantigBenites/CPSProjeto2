import time, random



def updateTemperature(inputSocket,newTemp):

        
    print(f"Updating temp to {newTemp}")
    inputSocket.send(str(newTemp).encode('utf8'))

def getTemperature(outputSocket,buffer):
    while True:
        try:
            data = outputSocket.recv(1024).decode()  # receive response
            buffer.append(data)  # show in terminal
            time.sleep(5)
        except Exception:
            pass



