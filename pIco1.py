from machine import UART, Pin, PWM
import time
time.sleep(1)  # Allow time for Pico 2 to initialize and be ready to receive the first target.

#PWM signal at GPIO 18 
pwm = PWM(Pin(0))
pwm.freq(1000)


#UART configuration for communication with Pico 2
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=100)



while True:
    # Get a valid target duty cycle from the user.
    while True:

        #ask the user for a target duty cycle between 0 and 100 and validate the input.
        try:
            target_duty = float(input("Enter target duty cycle (0-100): "))
            
            if 0<= target_duty <= 100:
                break
            else:
                print("Range error: Enter a value between 0-100")

        except ValueError:
            print("Invalid input: Please enter a number between 0-100.")

    # Send the target duty cycle to Pico 2 via UART.
    uart.write(str(target_duty) + "\n")

    # generate the pwm signal
    pwm.duty_u16(round(target_duty * 65535 / 100))

   
    # ----Waiting for pico 2 answer---

    # start the timer to wait for the response from Pico 2
    start = time.ticks_ms() 
    received_error = False

    # using interval of 5 seconds to wait for the response from Pico 2
    while time.ticks_diff(time.ticks_ms(), start) < 5000:

        if uart.any(): #check if anything was sent on the uart 
            message = uart.readline() # recieve the message or receive None

            if message: # if there is a message 
                try:
                    error = float(message.decode().strip()) #convert it from the binary to float 
                    print("Error received from Pico 2:", error)
                    received_error = True
                    break

                except ValueError: #in case there is an invalid response sent in the uart 
                    print("Invalid response from pico2")

        time.sleep_ms(10)

    #if the loop end and pico1 didnt receive a message of the error
    if not received_error:
        print("Pico 2 didnt respond within 5 seconds.")
