# Write your code here :-)

import PyLidar3
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


#Less than 150 cm --> Ultrasonic

    #Use basic operations to
