# Write your code here :-)

#Ultrasonic Test

import Ultrasonic_Class #Declared as class HCSR04

trig_pinR = pin(33, pin.OUT)
echo_pinR = pin(27, pin.IN)
trig_pinL = pin(32, pin.OUT)
echo_pinL = pin(15, pin.IN)
#trig_pinB = 5
#echo_pinB = 6

US_ObjR = Ultrasonic_Class.HCSR04(trig_pinR, echo_pinR)
US_ObjL = Ultrasonic_Class.HCSR04(trig_pinL, echo_pinL)
#US_ObjB = Ultrasonic_Class.HCSR04(trig_pinB, echo_pinB)

distR = US_ObjR.distance_cm()
distL = US_ObjL.distance_cm()
#distB = US_ObjB.distance_cm()

print("distance from right ultrasonic: " + distR + " cm")
print("distance from left ultrasonic:" + distL + "cm")
