from machine import UART, Pin, PWM
import time
time.sleep(1)  # Allow time for Pico 2 to initialize and be ready to receive the first target.

#PWM signal at GPIO 18 
pwm = PWM(Pin(18))
pwm.freq(1000)


#UART configuration for communication with Pico 2
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=2000)



while True:
    # Get a valid target duty cycle from the user.
    while True:
        try:
            entered_value = input("Enter target duty cycle (0-100): ")
            target_duty = float(entered_value)
            if target_duty < 0 or target_duty > 100:
                print("Invalid input. Please enter a number between 0 and 100.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number. between 0 and 100.")

    

    pwm.duty_u16(round(target_duty * 65535 / 100))

    # Send the target duty cycle to Pico 2 via UART.
    uart.write(str(target_duty) + "\n")

    # Wait for Pico 2 to return the error for this target.
    response_started = time.ticks_ms()
    received_error = False
    while time.ticks_diff(time.ticks_ms(), response_started) < 5000:
        if uart.any():
            error_message = uart.readline()
            if error_message:
                error_value = float(error_message)
                print("Error received from Pico 2:", error_value)
                received_error = True
                break
        time.sleep_ms(10)
    if not received_error:
        print("No valid error response from Pico 2 within 5 seconds.")
