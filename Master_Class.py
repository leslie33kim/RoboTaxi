from time import sleep
from time import sleep_us
from machine import Pin
from machine import time_pulse_us

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
    self.pin1.value(1)
    self.pin2.value(0)
    
  def backward(self, speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)

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
    
class Maneuver:
    def __init__(self, dc_motorL, dc_motorR):
        self.dc_motorL = dc_motorL
        self.dc_motorR = dc_motorR

    def maneuver_L(self):
        self.dc_motorR.forward(60)
        self.dc_motorL.forward(100)
        sleep(1.7)
        self.dc_motorL.stop()
        self.dc_motorR.stop()

        # self.dc_motorR.forward(100)
        # self.dc_motorL.forward(60)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

        # self.dc_motorR.forward(100)
        # self.dc_motorL.forward(60)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

    def maneuver_R(self):
        self.dc_motorR.forward(100)
        self.dc_motorL.forward(60)
        sleep(1.7)
        self.dc_motorL.stop()
        self.dc_motorR.stop()

        # self.dc_motorR.forward(60)
        # self.dc_motorL.forward(100)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

        # self.dc_motorR.forward(60)
        # self.dc_motorL.forward(100)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

    def maneuver_F(self):
        self.dc_motorR.forward(100)
        self.dc_motorL.forward(100)
        sleep(1.7)
        self.dc_motorL.stop()
        self.dc_motorR.stop()

        # self.dc_motorR.forward(60)
        # self.dc_motorL.forward(100)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

        # self.dc_motorR.forward(60)
        # self.dc_motorL.forward(100)
        # sleep(1.7)
        # self.dc_motorL.stop()
        # self.dc_motorR.stop()

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin.
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms
    
#Obstacle Detection Logic
#Beyond 150 cm --> Lidar
    #Use clustering logic to decide if there is a significant object
        #Include: approximate size(height and width), center location (x, y)
    #Big fat L, couldn't get the Lidar data onto the ESP32 without a ton of coding creating a micropython library for it
#Less than 10 cm --> perform manuever around the object
class Obstacle_Avoidance:

#Constructor - need to pass in ultrasonic class object and maneuver class object
    def __init__(self, ultras_objL, ultras_objR, ultras_objF, man_obj):
        self.ultrasonic_objL = ultras_objL
        self.ultrasonic_objR = ultras_objR
        self.ultrasonic_objF = ultras_objF
        self.maneuver_obj = man_obj

#Class Functions
    def check_surroundings(self):
        distL = self.ultrasonic_objL.distance_cm()
        distR = self.ultrasonic_objR.distance_cm()
        distF = self.ultrasonic_objF.distance_cm()
        msgL = ""
        msgR = ""
        msgF = ""
        flag = False

        if distL < 10 and distL > 0 and flag != True:  #Checks if dist is less than 10 cm
            msgL = "Avoiding object on left"
            print(msgL)
            self.maneuver_obj.maneuver_R() #Turn right
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_L() #Turn left
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_L() #Turn left
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_R() #Turn right
            flag = True

        elif distR < 10 and distR > 0 and flag != True:  #Checks if dist is less than 10 cm
            msgR = "Avoiding object on right"
            print(msgR)
            self.maneuver_obj.maneuver_L() #Turn left
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_R() #Turn right
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_R() #Turn right
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_L() #Turn left
            flag = True

        elif distF < 10 and distF > 0 and flag != True:  #Checks if dist is less than 10 cm
            msgF = "Avoiding object in front"
            print(msgF)
            self.maneuver_obj.maneuver_R() #Turn right
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_L() #Turn left
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_L() #Turn left
            self.maneuver_obj.maneuver_F() #Go forward
            self.maneuver_obj.maneuver_R() #Turn right
            flag = True

        return msgL + msgR + msgF
