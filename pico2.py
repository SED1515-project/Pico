from machine import ADC, Pin, UART



# ADC for voltage measurement on GPIO 26
adc = ADC(Pin(26))

#UART from pico2 with GPIO 0 as the transmitter and GPIO 1 as the receptor
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
