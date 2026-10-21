import time
#giving time for pico2 to start
time.sleep(0.1)

from machine import UART, ADC, Pin


uart = UART(1,baudrate=9600,tx = Pin(8), rx=Pin(9))

while True:
   #checking the message was sent to the uart conection yet if not wait 5 sec before checking again
   while True:
      targetvalue=uart.readline()
      if targetvalue is not None:
         print("received pico 1 desired value: ",targetvalue)
         break
      else:
         time.sleep(5)   
         continue

   # we initialize the pin that gonna read the signal

   adc= ADC(Pin(26))

   #giving time for the ADC reader to fix at one value 
   time.sleep_ms(500) 


   #measure the signal in percentage
   measured_signal= (adc.read_u16())*100 / 65535

   #calculate the error:

   error = float(targetvalue) - measured_signal

   #sending it using uart to pico1

   uart.write((str(error) + "\n").encode())







while True:
    #demander a l'utilisateur un message a envoyer
    timer = time.ticks_ms()
    while True:
        # while with timeout options
        while time.ticks_ms() <= 10000:
            envoyer=input("Entrer votre meessage: ")
        # check if the message exist
        if envoyer is not None:
            uart.write(envoyer)
            break
        # send a status update to the other user
        if timer>10000:
            uart.write("maintien de connexion ")
            
        





    #envoyer le message avec UART

    uart.write(envoyer)

    #recevoir 

    while True:
        recu = uart.read()
        if recu is not None:
            print(recu)
            break
        else:
            time.sleep(10)

    
  

