import tkinter as tk
from server import * 
from serverInterface import updateTemperature, getTemperature
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.dates as mdates
import datetime
from datetime import datetime

class App:

    def __init__(self, master):

        # Constants
        picoIP = "192.168.43.144"
        picoInputSocket = 5555
        picoOutputSocket = 4444

        # Connect to input
        self.inputSocket = connect_to_remote_socket(picoIP,picoInputSocket)
        
        # Connect to Output
        self.outputSocket = connect_to_remote_socket(picoIP,picoOutputSocket)
        
        # Temperature Data
        self.temperatureData = {'time': [],
         'temperature': [],
         'expected_temperature' : []
        }

        # Page
        self.window = master
        self.window.geometry("750x250")
        self.window['background']='#405169'

        self.left = tk.Frame(self.window)
        self.left.pack_propagate(0)
        self.left.pack(fill='both', side='left', expand=True)

        self.inputFrame = tk.Frame(self.left)
        self.inputFrame.pack(expand=True)

        self.right = tk.Frame(self.window)
        self.right.pack_propagate(0)
        self.right.pack(fill='both', side='right', expand=True)

        self.graphFrame = tk.Frame(self.right)
        self.graphFrame.pack(expand=True)

        self.currentExpectedTemp = 0


    def StartUpdateButtonEntry(self):

        temperatureInput = tk.IntVar()
        temp_entry = tk.Entry(master=self.inputFrame, textvariable=temperatureInput) 

        def updateButton():
            self.currentExpectedTemp = float(temp_entry.get())
            updateTemperature(self.inputSocket , temp_entry.get()) 
    
        button1 = tk.Button(master=self.inputFrame,text='Update Temperature', command=lambda : updateButton())

        temp_entry.pack()
        button1.pack()

    def StartShowTemperature(self):

        self.temp_label = tk.Label(self.inputFrame, text="Starting...", width=80, height=2, fg="green", font=('arial', 13)) 
        self.temp_label.pack()

    def StartTemperatureGraph(self):

        data = self.temperatureData
        
        # Start figure
        figure = plt.figure(figsize=(6,5), dpi=100)
        self.ax = figure.add_subplot(111)

        # Configure x-ticks
        self.ax.set_xticks(data['time']) # Tickmark + label at every plotted point
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        self.ax.set_ylabel('Temperature over time')

        self.ax.plot_date(data['time'], data['temperature'], ls='-', marker='o', color = "red", label='current_temperature')
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['expected_temperature'], ls='-', marker='o', color = "blue", label='expect_temperature')
        self.ax.grid(True)

        # Format the x-axis for dates (label formatting, rotation)
        figure.autofmt_xdate(rotation=45)
        figure.tight_layout()


        # Start Figure canvas in tk
        self.temperatureChart = FigureCanvasTkAgg(figure, self.graphFrame)
        self.temperatureChart.get_tk_widget().pack()

    def updateChart(self):

        data = self.temperatureData

        self.ax.plot_date(data['time'], data['temperature'], ls='-', marker='o', color = "red")
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['expected_temperature'], ls='-', marker='o', color = "blue")
        self.ax.grid(True)

        self.temperatureChart.draw()



root = tk.Tk()

app = App(root)

app.StartUpdateButtonEntry()

app.StartShowTemperature()

app.StartTemperatureGraph()

buffer:list[str] = []

x = threading.Thread(target=getTemperature, args=(app.outputSocket,buffer))
x.start()
lastime = time.time()

while True:
    #time.sleep(2)
    
    # Print latest temperature
    if time.time() - lastime > 2:
        lastime = time.time()
        try:
            
            # Update text
            temperatureList = buffer[-2].split("\n")[:-1]
            currentTimeTemperature = temperatureList[-1]
            time_string = currentTimeTemperature.split(" , ")[0]
            temperature_string = currentTimeTemperature.split(" , ")[1]
            app.temp_label[ "text" ]=f"At time {time_string} temperature is {temperature_string} \n Trying to go to {app.currentExpectedTemp}"

            # Update dataFrame

            # Time
            x_time = mdates.date2num(datetime.strptime(time_string,"%H:%M:%S"))

            # Temperature
            x_temperature = float(temperature_string)

            # Update dataframe
            app.temperatureData["time"].append(x_time)
            app.temperatureData["temperature"].append(int(x_temperature))
            app.temperatureData["expected_temperature"].append(app.currentExpectedTemp)
            app.updateChart()

        except Exception:
            pass

    root.update()

root.mainloop()
