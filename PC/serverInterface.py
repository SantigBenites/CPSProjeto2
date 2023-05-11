import time, random



def updateTemperature(inputSocket,newTemp):

        
    inputSocket.send(str(newTemp).encode('utf8'))

def getTemperature(outputSocket,buffer):
    while True:
        try:
            data = outputSocket.recv(1024).decode()  # receive response
            buffer.append(data)  # show in terminal
            time.sleep(2)
        except Exception:
            pass



