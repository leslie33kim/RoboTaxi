import network
import socket
import binascii

import gc
gc.collect()

import esp
esp.osdebug(None)

from machine import Pin, PWM   
from time import sleep

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

# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect('Berkeley-IoT', '4,pEg&"W') # connect to an AP
# wlan.config('mac')      # get the interface's MAC address
# print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)
macaddress = (ap.config('mac'))
print(macaddress)


# mac_str = binascii.hexlify(ap.config('mac')).decode()
# print(mac_str)

ap.config(essid='ESP32-RoboTaxi',password='RoboTaxi') # set the SSID of the access point
print(ap.config('essid'))
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)         # activate the interface

print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Hello, World! This is your ESP32 Talking</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for AP
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for Berkeley-IoT
s.bind(('', 80))
s.listen(30)
print('socket')

print('before running motors')
frequency = 15000       
pinLf = Pin(4, Pin.OUT) #left wheel forward
pinLb = Pin(5, Pin.OUT) #left wheel backward
enableL = PWM(Pin(13), frequency) #left wheel PWM
pinRf = Pin(18, Pin.OUT) #right wheel forward
pinRb = Pin(19, Pin.OUT) #right wheel backward
enableR = PWM(Pin(12), frequency) #right wheel PWM

dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)

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
        # dc_motorL.forward(0) 
        dc_motorR.forward(100)
    elif Command == 'D':
        response = 'Right'
        conn.send(response)
        dc_motorL.forward(100) 
        # dc_motorR.forward(0)
    elif Command == 'E':
        response = 'Stop'
        conn.send(response)
        dc_motorL.stop() 
        dc_motorR.stop()
    elif Command == 'F': # Track 1
        response = 'Track 1'
        conn.send(response)
        # Straight run from (0,0)
        dc_motorL.forward(100) 
        dc_motorR.forward(100)
        for i in range(50):
            conn.close()
            conn, addr = s.accept()
            request = conn.recv(1024)
            Command=str(request)[2]
            if Command == 'E':
                dc_motorL.stop() 
                dc_motorR.stop()
                break
            sleep(0.1)
        if Command == 'E':
            conn.close()
            continue
        dc_motorL.stop()
        dc_motorR.stop()
        # First semi-circle
        dc_motorL.forward(100)  
        # dc_motorR.forward(0)
        sleep(5)
        dc_motorL.stop()
        dc_motorR.stop()
        # Straight run after first semi-circle
        dc_motorL.forward(100) 
        dc_motorR.forward(100)
        sleep(5)
        dc_motorL.stop()
        dc_motorR.stop()
        # Second semi-circle to close the loop
        dc_motorL.forward(100)  
        # dc_motorR.forward(0)
        sleep(5)
        dc_motorL.stop()
        dc_motorR.stop()
    elif Command == 'G': # Track 2
        response = 'Track 2'
        conn.send(response)
        # Circular-loop
        dc_motorL.forward(100)  
        # dc_motorR.forward(0)
    conn.close()

