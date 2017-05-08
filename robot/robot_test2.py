from machine import Pin as pin
import time

p0 = pin(0,pin.OUT) # motor left direction
p2 = pin(2,pin.OUT) # motor right direction
p4 = pin(4,pin.OUT) # motor right enable
p5 = pin(5,pin.OUT) # motot left enable

def rightWheelForward(seconds):
    for i in list(range(1,seconds + 1)):
        p2.high(); p4.high()
        time.sleep(1)
    
def rightWheelBackwards(seconds):
    for i in list(range(1,seconds + 1)):
        p2.low(); p4.high()
        time.sleep(1)

def stopRightWheel():
    p2.low();p4.low()    
        
def leftWheelForward(seconds):
    for i in list(range(1,seconds + 1)):
        p0.high(); p5.high()
        time.sleep(1)
    
def leftWheelBackwards(seconds):
    for i in list(range(1,seconds + 1)):
        p0.low(); p5.high()
        time.sleep(1)

def stopLeftWheel():
    p5.low();p0.low()  

def stopAll():
    stopLeftWheel()
    stopRightWheel()
  
def clearBuffer():
    p0.low()
    p2.low()
    p4.low()
    p5.low()
    
def moveForward(seconds):
    clearBuffer()
    for i in list(range(1,seconds + 1)):
        p2.high(); p4.high()
        p0.high(); p5.high()
        time.sleep(1)
    stopAll()
        
#rightWheelForward(5)
#rightWheelBackwards(5)
#stopRightWheel()
#leftWheelForward(5)
#leftWheelBackwards(5)
#stopLeftWheel()
moveForward(10)
