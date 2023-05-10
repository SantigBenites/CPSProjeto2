from machine import Pin, PWM

def updateTemperature(buffer):

    warmPin = PWM(Pin(15))
    coldPin = PWM(Pin(15))

    print("Updating temperature")
    warmPin.freq(1000)
    coldPin.freq(1000)

    while True:

        if len(buffer) != 0:

            (newTemp,currentTemp) = buffer.pop()
            print(f"We are at {currentTemp} and we want to go to {newTemp}")
            if newTemp > currentTemp:
                print("Getting colder")
                coldPin.duty_u16(65025)
            else:
                print("Getting warmer")
                warmPin.duty_u16(65025)
            