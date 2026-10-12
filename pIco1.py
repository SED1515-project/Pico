import time
from machine import UART, Pin, PWM

#pico1 

#UART 1 transmitter & receptor 
pin_tx1 = 0
pin_rx1 = 1
#UART 2 trasmitter & receptor
pin_tx2 = 0
pin_rx2 = 0

#PWM signal for pico1
pwm = PWM(Pin(18))
pwm.freq(1000)
pwm.duty_u16(32768)

