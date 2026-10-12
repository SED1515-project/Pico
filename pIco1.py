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

while True:
    #UART 1 communication
    uart1 = UART(0, baudrate=9600, tx=Pin(pin_tx1), rx=Pin(pin_rx1))
    if uart1.any():
        message = uart1.readline()
        if message:
            try:
                text = message.decode().strip()
                if text.startswith("SET:"):
                    target_duty = max(0.0, min(100.0, float(text[4:])))
                    pwm.duty_u16(round(target_duty * 65535 / 100))
            except (UnicodeError, ValueError):
                print("Message UART invalide:", message)
    
    #UART 2 communication
    uart2 = UART(1, baudrate=9600, tx=Pin(pin_tx2), rx=Pin(pin_rx2))
    if uart2.any():
        response = uart2.readline()
        if response:
            try:
                message = response.decode().strip()
                if message.startswith("ERR:"):
                    error = float(message[4:])
                    print("Erreur (consigne - mesure): {:.2f}%".format(error))
            except (UnicodeError, ValueError):
                print("Message UART invalide:", response)
    
    time.sleep_ms(10)
