import Master_Class

trig_pinR = 33
echo_pinR = 27
trig_pinL = 32
echo_pinL = 15
trig_pinB = 22
echo_pinB = 14

US_SensorR = Master_Class.HCSR04(trigger_pin = trig_pinR, echo_pin = echo_pinR, echo_timeout_us=10000)
US_SensorL = Master_Class.HCSR04(trigger_pin = trig_pinL, echo_pin = echo_pinL, echo_timeout_us=10000)
US_SensorF = Master_Class.HCSR04(trigger_pin = trig_pinB, echo_pin = echo_pinB, echo_timeout_us=10000)

frequency = 15000       
pinLf = Pin(4, Pin.OUT) #left wheel forward
pinLb = Pin(5, Pin.OUT) #left wheel backward
enableL = PWM(Pin(13), frequency) #left wheel PWM
pinRf = Pin(18, Pin.OUT) #right wheel forward
pinRb = Pin(19, Pin.OUT) #right wheel backward
enableR = PWM(Pin(12), frequency) #right wheel PWM

dc_motorL = Master_Class.DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorR = Master_Class.DCMotor(pinRf, pinRb, enableR, 350, 1023)

maneuver = Master_Class.Maneuver(dc_motorL, dc_motorR)

avoidance = Master_Class.Obstacle_Avoidance(US_SensorL, US_SensorR, US_SensorF, maneuver)

while True:
    dc_motorR.forward(100)
    dc_motorR.forward(100)
    avoidance.check_surroundings_dynamic()
    dc_motorR.stop()
    dc_motorL.stop()