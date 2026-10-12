import time
from machine import UART, Pin, PWM


#PWM signal from GPIO 18 to pico2
pwm = PWM(Pin(18))
pwm.freq(1000)
pwm.duty_u16(32768)

#UART from pico1 with GPIO 0 as the transmitter and GPIO 1 as the receptor
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

