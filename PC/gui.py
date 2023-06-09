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
        picoIP = "192.168.43.179"
        picoInputSocket = 5555
        picoOutputSocket = 4444

        # Connect to input
        self.inputSocket = connect_to_remote_socket(picoIP,picoInputSocket)
        
        # Connect to Output
        self.outputSocket = connect_to_remote_socket(picoIP,picoOutputSocket)
        
        # Temperature Data
        self.temperatureData = {'time': [],
         'temperature': [],
         'ambient_temperature': [],
         'expected_temperature' : []
        }

        # Page
        self.window = master
        self.window.geometry("750x250")
        self.window['background']='#405169'

        self.left = tk.Frame(self.window)
        self.left.pack(fill='both', side='top', expand=True)
        self.left.pack_propagate(0)

        self.inputFrame = tk.Frame(self.left)
        self.inputFrame.pack(expand=True)

        self.right = tk.Frame(self.window)
        self.right.pack(fill='both', side='bottom', expand=True)
        self.right.pack_propagate(0)

        self.graphFrame = tk.Frame(self.right)
        self.graphFrame.pack(expand=True)

        self.currentExpectedTemp = 0

        self.StartUpdateButtonEntry()
        self.StartShowTemperature()
        self.StartTemperatureGraph()

    def update_loop(self, buffer):
            
        try:

            # Update text
            
            temperatureList = buffer[-2].split("\n")[:-1]
            if len(temperatureList) > 0:
                currentTimeTemperature = temperatureList[-1]
                time_string = currentTimeTemperature.split(" , ")[0]
                temperature_string = currentTimeTemperature.split(" , ")[1]
                ambient_temp_string = currentTimeTemperature.split(" , ")[2]
                self.temp_label[ "text" ]=f"At time {time_string} temperature is {temperature_string} \n Trying to go to {self.currentExpectedTemp} \n Ambient temperature is {ambient_temp_string}"

                # Update dataFrame

                # Time
                x_time = mdates.date2num(datetime.strptime(time_string,"%H:%M:%S"))

                # Temperature
                x_temperature = float(temperature_string)
                x_ambient_temperature = float(ambient_temp_string)

                # Update dataframe
                self.temperatureData["time"].append(x_time)
                self.temperatureData["temperature"].append(float(x_temperature))
                self.temperatureData["ambient_temperature"].append(float(x_ambient_temperature))
                self.temperatureData["expected_temperature"].append(self.currentExpectedTemp)
                self.updateChart()
                print("updating")

        except Exception:
            pass

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

        self.temp_label = tk.Label(self.inputFrame, text="Starting...", width=100, height=5, fg="green", font=('arial', 13)) 
        self.temp_label.pack()

    def StartTemperatureGraph(self):

        data = self.temperatureData
        
        # Start figure
        figure = plt.figure(figsize=(16,5), dpi=100)
        self.ax = figure.add_subplot(111)

        # Configure x-ticks
        self.ax.set_xticks(data['time']) # Tickmark + label at every plotted point
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

        self.ax.plot_date(data['time'], data['temperature'], color = "red", label='current_temperature')
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['expected_temperature'], color = "blue", label='expect_temperature')
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['ambient_temperature'], color = "green", label='ambient_temperature')
        self.ax.grid(True)

        # Format the x-axis for dates (label formatting, rotation)
        figure.autofmt_xdate(rotation=45)
        figure.tight_layout()


        # Start Figure canvas in tk
        self.temperatureChart = FigureCanvasTkAgg(figure, self.graphFrame)
        self.temperatureChart.get_tk_widget().pack()

    def updateChart(self):

        data = self.temperatureData

        plt.style.use('ggplot')


        self.ax.set_ylabel('Temperature')
        self.ax.set_xlabel('Time')


        self.ax.plot_date(data['time'], data['temperature'], fmt="b", ls='-', marker=None)
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['expected_temperature'], fmt="r", ls='-', marker=None)
        self.ax.grid(True)

        self.ax.plot_date(data['time'], data['ambient_temperature'], fmt="g", ls='-', marker=None)
        self.ax.grid(True)

        self.temperatureChart.draw()



root = tk.Tk()

app = App(root)

buffer:list[str] = []
temperatureThread = threading.Thread(target=getTemperature, args=(app.outputSocket,buffer))
temperatureThread.start()


while True:
    
    app.update_loop(buffer)
    root.update()