from machine import Pin, PWM

def updateTemperature(buffer):

    #warmPin = PWM(Pin(15))
    coldPin = PWM(Pin(15))

    print("Updating temperature")
    #warmPin.freq(1000)
    coldPin.freq(1000)

    while True:

        if len(buffer) != 0:

            (newTemp,currentTemp) = buffer.pop()
            if newTemp > currentTemp:
                print(f"We are at {currentTemp} and we want to go to {newTemp} getting colder")
                coldPin.duty_u16(65025)
            else:
                print(f"We are at {currentTemp} and we want to go to {newTemp} getting warmer")
                coldPin.duty_u16(0)
            