import time
#giving some time for the pico to bootup
time.sleep(0.1)
from machine import UART, Pin, PWM


#creating the UART connection

uart= UART(1,baudrate=9600, tx=Pin(8), rx=Pin(9))

#the pwm signal gonna be sent using the pin 18 on the pico and we gonna set it to 1000HZ
pwm = PWM(Pin(18))
pwm.freq(1000)


while True:

    #get a value from the user between 0-100% and use it as the frequency for the pwm signal 
    while True:
        try:
            percentage = float(input("Enter the desired frequency between 0-100%: "))
            if 0<= percentage <=100:
                uart.write(str(percentage))
                break
            else:
                print("choose a value between 0-100%")

        except ValueError:
            percentage = print("Enter a valid value between 0-100%")

    #sending the signal to pico 2 

    pwm.duty_u16(round(percentage * 65535 / 100))
    print("pico 1 sent the pwm signal at ",percentage, " %")

    #checking if pico 2 sent a message if not make the pico 1 check again after 5 sec
    counter = 0
    while counter<=60:
        print("pico 1 listening to an error message from pico 2")
        error = uart.readline()
        if error is not None :
            error = float(uart.readline().decode().strip())
            print("l'erreur est: ",error)
            break
        else:
            counter+=5
            print("no messages yet")
            time.sleep(5)
    if counter>60:
        print("pico 1 was unable to receieve any message from pico 2 after 1 min")
        break
