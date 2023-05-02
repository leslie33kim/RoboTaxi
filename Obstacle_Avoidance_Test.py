from machine import Pin, PWM   
from time import sleep

trig_pinR = 33
echo_pinR = 27
trig_pinL = 32
echo_pinL = 15
trig_pinB = 22
echo_pinB = 14

US_SensorR = HCSR04(trigger_pin = trig_pinR, echo_pin = echo_pinR, echo_timeout_us=10000)
US_SensorL = HCSR04(trigger_pin = trig_pinL, echo_pin = echo_pinL, echo_timeout_us=10000)
US_SensorF = HCSR04(trigger_pin = trig_pinB, echo_pin = echo_pinB, echo_timeout_us=10000)

frequency = 15000       
pinLf = Pin(4, Pin.OUT) #left wheel forward
pinLb = Pin(5, Pin.OUT) #left wheel backward
enableL = PWM(Pin(13), frequency) #left wheel PWM
pinRf = Pin(18, Pin.OUT) #right wheel forward
pinRb = Pin(19, Pin.OUT) #right wheel backward
enableR = PWM(Pin(12), frequency) #right wheel PWM

dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)

maneuver = Maneuver(dc_motorL, dc_motorR)

avoidance = Obstacle_Avoidance(US_SensorL, US_SensorR, US_SensorF, maneuver)

# Straight run from (0,0)
while(1):
  dc_motorL.forward(100) 
  dc_motorR.forward(100)
  avoidance.check_surroundings()