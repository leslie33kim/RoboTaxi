from machine import Pin, PWM   
from time import sleep

class DCMotor:      
  def __init__(self, pin1, pin2, enable_pin, min_duty=750, max_duty=1023):
    self.pin1=pin1
    self.pin2=pin2
    self.enable_pin=enable_pin
    self.min_duty = min_duty
    self.max_duty = max_duty

  def forward(self,speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)
    
  def backward(self, speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)

  def stop(self):
    self.enable_pin.duty(0)
    self.pin1.value(0)
    self.pin2.value(0)
    
  def duty_cycle(self, speed):
    if self.speed <= 0 or self.speed > 100:
      duty_cycle = 0
    else:
      duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed-1)/(100-1)))
      return duty_cycle

frequency = 15000       
pinLf = Pin(4, Pin.OUT) #left wheel forward
pinLb = Pin(5, Pin.OUT) #left wheel backward
enableL = PWM(Pin(13), frequency) #left wheel PWM
pinRf = Pin(18, Pin.OUT) #right wheel forward
pinRb = Pin(19, Pin.OUT) #right wheel backward
enableR = PWM(Pin(12), frequency) #right wheel PWM

dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)

# Straight run from (0,0)
dc_motorL.forward(100) 
dc_motorR.forward(100)
sleep(20)

# First semi-circle
dc_motorL.forward(100)  
dc_motorR.forward(60)
sleep(10)

# Straight run after first semi-circle
dc_motorL.forward(100) 
dc_motorR.forward(100)
sleep(20)

# Second semi-circle to close the loop
dc_motorL.forward(100)  
dc_motorR.forward(60)
sleep(10)
dc_motorL.stop()
dc_motorR.stop()
