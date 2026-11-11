import time
from machine import UART, Pin, I2C

# INITIALISATION ET CONFIGURATION DES DONNEES
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=1000)
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=100000)
ADS1015 = 0x48          # Adresse de la puce ADS1015 sur le Pico
time.sleep(1) 

def read_voltage():
  
    """Cette fonction convertit le signal analogique 
    en numérique par la puce ADS1015 et retourne la 
    tension mesurée en volts."""

  # Ecrit dans le registre de configuration de l'ADS1015
  i2c.writeto_mem(ADS1015, 0x01, bytes([0xE3, 0x83]))
  time.sleep_ms(10)                                      # Attente de la fin de la conversion
 
  # Lecture du registre de sortie de la conversion
  data = i2c.readfrom_mem(ADS1015, 0x00, 2)

  # Extraction de la valeur ADC sur 12 bits
  raw = ((data[0] << 8) | data[1]) >> 4

  # Gestion du signe (complément à 2)
  if raw & 0x800:
    raw = raw - 4096
  # Conversion en tension : 1 LSB = 2 mV avec gain ±4.096V
  return raw * 0.002


  # Mesurer ce qui s'echappe du filtre RC et renvoyer l'ecart a Pico1
while True:

    #Verifier si le message duty_cycle envoye par Pico1 est correct:
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

