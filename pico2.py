from machine import ADC, Pin, UART
import time
time.sleep(1)  # Allow time for Pico 1 to initialize and send the first target.



#UART configuration for communication with Pico 2
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


# ADC for voltage measurement on GPIO 26
adc = ADC(Pin(26))

while True:
    # Read a target value from Pico 1 via UART.
    message = None
    while message is None:
        if uart.any():
            message = uart.readline()
            if message:
                target_duty = float(message)
        if not message:
            message = None
            time.sleep_ms(10)


    # Let the RC-filtered PWM voltage settle before measuring.
    time.sleep_ms(500)
    measured_voltage = adc.read_u16() * 3.3 / 65535
    measured_duty = max(0.0, min(100.0, measured_voltage * 100 / 3.3))

    error = target_duty - measured_duty
    print("Measured duty cycle:", measured_duty)
    print("Error (target - measured):", error)
    uart.write(str(error) + "\n")
