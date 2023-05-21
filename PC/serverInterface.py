import time, random
import pandas as pd
import matplotlib.dates as mdates
import datetime
import json
import socket


def updateTemperature(inputSocket,newTemp):

        
    inputSocket.send(str(newTemp).encode('utf8'))

def getTemperature(outputSocket:socket.socket,buffer):
    while True:
        try:
            data = outputSocket.recv(1024).decode()  # receive response
            buffer.append(data)  # show in terminal
            print(data)
            time.sleep(2)
        except Exception:
            pass




