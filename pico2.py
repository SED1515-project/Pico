import time
time.sleep(1)

from machine import UART, Pin, I2C


#UART configuration
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=1000)

#I2C configuration
i2c = I2C(1, sda = Pin(14), scl=Pin(15), freq=100000)

#ADS chip address on the extended pico board
ADS1015 = 0x48

def read_voltage():
    """Convert the analog signal to digital using ADS1015 chip
    
    return the voltage"""

    #write to the ADS1015 configuration register:
    i2c.writeto_mem(ADS1015, 0x01, bytes([0xE3,0x83]))

    #we wait for the conversion
    time.sleep_ms(10)

    #read the digital output from the conversion register
    data = i2c.readfrom_mem(ADS1015, 0x00, 2)
    
    #Extract 12 bit ADC value 
    raw = ((data[0] << 8) | data[1]) >> 4

    if raw & 0x800:
        raw-=4096

    return raw * 0.002



while True:

    #Check if pico1 sent the desired duty_cycle message:
    while True:
        message = (uart.readline())
        if message:
            break
    target_duty = float(message.decode().strip())

    # doing an average voltage after 50 measurement of the same 
    total = 0

    for i in range(50):

        total += read_voltage()
    
    measured_voltage = total/50

    #convert the voltage to a percentage of the duty cycle 
    measured_duty = (measured_voltage / 3.3) / 100

    # shows the amount of duty cycle lost in the process 
    error = target_duty - measured_duty

    #send the error to pico1
    uart.write(str(error).encode())
