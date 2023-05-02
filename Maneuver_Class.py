# Write your code here :-)
import Ultrasonic_Class #Declared as class HCSR04
import DCmotor

class Maneuver:

    def __init__(self, maneuver_L, maneuver_R, maneuver_F, man_obj):
        self.maneuver_obj.maneuverL = maneuver_L
        self.maneuver_obj.maneuverR = maneuver_R
        self.maneuver_obj.maneuverF = maneuver_F
        self.maneuver_obj = man_obj

    def maneuver_L(self):
    dc_motorL.forward(30)
    dc_motorR.forward(60)
#    sleep(10)


    def maneuver_R(self):
    dc_motorL.forward(60)
    dc_motorR.forward(30)
#    sleep(10)



    def maneuver_F(self):
    dc_motorL.forward(100)
    dc_motorR.forward(100)
#    sleep(10)
