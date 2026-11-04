import time

# Allow time for Pico 1 to initialize and send the first target.
time.sleep(1)

from machine import ADC, Pin, UART
  



#UART configuration for communication with Pico 2
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))


# ADC for voltage measurement on GPIO 26
adc = ADC(Pin(26))

while True:
    # Read a target value from Pico 1 via UART.
    message = None

    while message is None:
        message = uart.readline()

        if message is None:  
             time.sleep_ms(10)   

    target_duty = float(message.decode().strip())
    print("voici la valeur envoyer par pico 1 sur UART: ",target_duty)

    # Let the RC-filtered PWM voltage settle before measuring.
    time.sleep_ms(500)

    # Measure the average voltage
    measured_voltage = adc.read_u16() * 3.3 / 65535
    
    # Convert the voltage into a duty cycle percentage 
    measured_duty = max(0.0, min(100.0, measured_voltage * 100 / 3.3))

    error = target_duty - measured_duty
    print("Measured duty cycle:", measured_duty)
    print("Error (target - measured):", error)
    uart.write(str(error) + "\n")

