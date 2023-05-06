# Write your code here :-)
import DCmotor

class Maneuver:
    def __init__(self, dc_motorL, dc_motorR):
        self.dc_motorL = dc_motorL
        self.dc_motorR = dc_motorR

    def maneuver_L(self):
        dc_motorR.forward(60)
        dc_motorL.forward(100)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(100)
        dc_motorL.forward(60)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(100)
        dc_motorL.forward(60)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

 
    def maneuver_R(self):
        dc_motorR.forward(100)
        dc_motorL.forward(60)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(60)
        dc_motorL.forward(100)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(60)
        dc_motorL.forward(100)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()


    def maneuver_F(self):
        dc_motorR.forward(100)
        dc_motorL.forward(60)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(60)
        dc_motorL.forward(100)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()

        dc_motorR.forward(60)
        dc_motorL.forward(100)
        sleep(1.7)
        dc_motorL.stop()
        dc_motorR.stop()
