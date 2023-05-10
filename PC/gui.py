import tkinter as tk
from server import * 
from serverInterface import updateTemperature, getTemperature
import threading

class App:

    def __init__(self, master):

        # Constants
        picoIP = "192.168.43.76"
        picoInputSocket = 5555
        picoOutputSocket = 4444

        # Connect to input
        self.inputSocket = connect_to_remote_socket(picoIP,picoInputSocket)
        
        # Connect to Output
        self.outputSocket = connect_to_remote_socket(picoIP,picoOutputSocket)
        
        # Page
        self.window = master
        self.window.geometry("750x250")


    def StartUpdateButtonEntry(self):

        temperatureInput = tk.IntVar()
        temp_entry = tk.Entry(master=self.window, textvariable=temperatureInput) 
    
        button1 = tk.Button(master=self.window,text='Update Temperature', command=lambda : updateTemperature(self.inputSocket , temp_entry.get()))

        temp_entry.pack()
        button1.pack()

    def StartShowTemperature(self):

        self.temp_label = tk.Label(self.window, text="Starting...", width=80, height=2, fg="green", font=('arial', 13)) 
        self.temp_label.pack()


root = tk.Tk()

app = App(root)

app.StartUpdateButtonEntry()

app.StartShowTemperature()

buffer = [0]

x = threading.Thread(target=getTemperature, args=(app.outputSocket,buffer))
x.start()

while True:
    time.sleep(1)
    app.temp_label[ "text" ]=f"Temperature is {buffer[-1]}"
    root.update()

root.mainloop()
