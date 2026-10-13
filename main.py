import time
time.sleep(1)  # Allow time for the Pico to initialize.

from machine import Pin


# GP2 is HIGH on Pico 1 (sender) and LOW on Pico 2 (receiver).
#choose which Pico to run based on the state of GP2.
if Pin(2, Pin.IN).value():
    import pico1
else:
    import pico2
