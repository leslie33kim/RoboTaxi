# Write your code here :-)

#Ultrasonic Test

import Ultrasonic_Class #Declared as class HCSR04

#trig_pinR = pin(33, pin.OUT)
#echo_pinR = pin(27, pin.IN)
#trig_pinL = pin(32, pin.OUT)
#echo_pinL = pin(15, pin.IN)
trig_pinR = 33
echo_pinR = 27
trig_pinL = 32
echo_pinL = 15
#trig_pinB = 5
#echo_pinB = 6

US_SensorR = Ultrasonic_Class.HCSR04(trigger_pin = trig_PinR, echo_pin = echo_pinR, echo_timeout_us=10000)
US_SensorL = Ultrasonic_Class.HCSR04(trigger_pin = trig_pinL, echo_pin = echo_pinL, echo_timeout_us=10000)
#US_SensorB = Ultrasonic_Class.HCSR04(trigger_pin = trig_pinB, echo_pin = echo_pinB, echo_timeout_us=10000)

#distR = US_SensorR.distance_cm()
#distL = US_SensorL.distance_cm()
#distB = US_SensorB.distance_cm()

While True:
    distR = US_SensorR.distance_cm()
    distL = US_SensorL.distance_cm()
    print("distance from right ultrasonic: " + distR + " cm")
    print("distance from left ultrasonic:" + distL + "cm")
