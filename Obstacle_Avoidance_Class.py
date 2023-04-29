# Write your code here :-)

#import PyLidar3
import Ultrasonic_Class #Declared as class HCSR04
import Maneuver_Class #Declared as class Maneuver

#Obstacle Detection Logic

#Case example - Arc maneuver around object
#-------------------------
#-----------------XXX-----
#-----------------XXX-----
#---Car..........-XXX-....
#----------------.---.----
#-----------------...----
#-------------------------

#Beyond 150 cm --> Lidar

    #Use clustering logic to decide if there is a significant object
        #Include: approximate size(height and width), center location (x, y)
#Lidar_Obj = PyLidar3.class()


#Less than 150 cm --> Ultrasonic
    #Use basic operations to detect object location and perform emergency maneuver

#Class Functions

trig_pin1 = 1
echo_pin1 = 2
trig_pin2 = 3
echo_pin2 = 4
trig_pin3 = 5
echo_pin3 = 6

US_Obj1 = Ultrasonic_Class.HCSR04(trig_pin1, echo_pin1)
US_Obj2 = Ultrasonic_Class.HCSR04(trig_pin2, echo_pin2)
US_Obj3 = Ultrasonic_Class.HCSR04(trig_pin3, echo_pin3)

dist1 = US_Obj1.distance_cm()
dist2 = US_Obj2.distance_cm()
dist3 = US_Obj3.distance_cm()
