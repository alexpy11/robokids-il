from machine import Pin as pin
import time
p16 = pin(16,pin.OUT)
p4 = pin(46,pin.OUT)
for i in [1, 2, 3, 4]:
    p16.high(); p4.low()
    time.sleep(1)
    p16.low(); p4.high()
    time.sleep(1)
