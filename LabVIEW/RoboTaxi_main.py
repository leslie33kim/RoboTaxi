import network
import socket
import binascii

import gc
gc.collect()

import esp
esp.osdebug(None)

from machine import Pin, PWM   
from time import sleep

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)
macaddress = (ap.config('mac'))
print(macaddress)

ap.config(essid='ESP32-RoboTaxi',password='RoboTaxi') # set the SSID of the access point
print(ap.config('essid'))
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)         # activate the interface

print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for AP
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for Berkeley-IoT
s.bind(('', 80))
s.listen(30)
print('socket')

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

threshold = 25

avoidance = Obstacle_Avoidance(US_SensorL, US_SensorR, US_SensorF, maneuver, threshold, dc_motorL, dc_motorR)

while(1):
    print('waiting for connection')
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    Command=str(request)[2]
    if Command == 'A':
        response = 'Forward'
        conn.send(response)
        dc_motorL.forward(100) 
        dc_motorR.forward(100)
    elif Command == 'B':
        response = 'Backward'
        conn.send(response)
        dc_motorL.backward(100) 
        dc_motorR.backward(100)
    elif Command == 'C':
        response = 'Left'
        conn.send(response)
        dc_motorL.forward(60) 
        dc_motorR.forward(100)
    elif Command == 'D':
        response = 'Right'
        conn.send(response)
        dc_motorL.forward(100) 
        dc_motorR.forward(60)
    elif Command == 'E':
        response = 'Stop'
        conn.send(response)
        dc_motorL.stop() 
        dc_motorR.stop()
    elif Command == 'F': # Track 1
        response = 'Track 1'
        conn.send(response)
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # First turn
        dc_motorL.forward(100)
        sleep(1.5)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Second turn
        dc_motorL.forward(100)
        sleep(1.5)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Third turn
        dc_motorL.forward(100)
        sleep(1.5)
        dc_motorL.stop() 
        dc_motorR.stop()
    elif Command == 'G': # Track 2
        response = 'Track 2'
        conn.send(response)
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # First turn
        dc_motorL.forward(100)
        sleep(1.1)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Second turn
        dc_motorL.forward(100)
        sleep(1.1)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Third turn
        dc_motorL.forward(100)
        sleep(1.1)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Forward
        dc_motorL.forward(100)
        dc_motorR.forward(100)
        sleep(4)
        dc_motorL.stop() 
        dc_motorR.stop()
        # Rotate 90 deg
        dc_motorL.forward(100)
        sleep(1.1)
        dc_motorL.stop()
        dc_motorR.stop()
    elif Command == 'H': # Interactive Mode
        while True:
            response = 'Interactive Mode'
            conn.send(response)
            # Forward
            dc_motorL.forward(100)
            dc_motorR.forward(100)
            for i in range(40):
                avoidance.check_surroundings()
                sleep(0.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # First turn
            dc_motorL.forward(100)
            # dc_motorR.forward(40)
            avoidance.check_surroundings()
            sleep(1.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Forward
            dc_motorL.forward(100)
            dc_motorR.forward(100)
            for i in range(40):
                avoidance.check_surroundings()
                sleep(0.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Second turn
            dc_motorL.forward(100)
            # dc_motorR.forward(40)
            avoidance.check_surroundings()
            sleep(1.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Forward
            dc_motorL.forward(100)
            dc_motorR.forward(100)
            for i in range(40):
                avoidance.check_surroundings()
                sleep(0.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Third turn
            dc_motorL.forward(100)
            # dc_motorR.forward(40)
            avoidance.check_surroundings()
            sleep(1.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Forward
            dc_motorL.forward(100)
            dc_motorR.forward(100)
            for i in range(40):
                avoidance.check_surroundings()
                sleep(0.1)
            dc_motorL.stop() 
            dc_motorR.stop()
            # Rotate 90 deg
            dc_motorL.forward(100)
            # dc_motorR.forward(0)
            avoidance.check_surroundings()
            sleep(1.1)
            dc_motorL.stop()
            dc_motorR.stop()
    elif Command == 'I': # Interactive Mode
        while True:
            response = 'Interactive Mode'
            conn.send(response)
            # Forward
            dc_motorL.forward(100)
            dc_motorR.forward(100)
            avoidance.check_surroundings_dynamic()
            dc_motorL.stop()
            dc_motorR.stop()

    conn.close()
