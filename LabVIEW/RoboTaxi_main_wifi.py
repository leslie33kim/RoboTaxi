# Load appropriate libraries
import network
import socket
import binascii

import gc
gc.collect()

import esp
esp.osdebug(None)

import time
import machine
from machine import Pin,Timer,PWM
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
    self.pin1.value(0)
    self.pin2.value(1)
    
  def backward(self, speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)

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

LED_BLINK_TIMER_CLOCK_ms = 1000
timer_period = 1000
led_blink_active_flag = 1
ledstate = 1
timer_interrupt_flag = 1

def toggle_led(timer):
    global ledstate
    ledstate = ledstate^1
    if led_blink_active_flag == 1:
        led(ledstate)

led = Pin(15, mode=Pin.OUT)
led(ledstate)
t1 = Timer(1)
t1.init(period=LED_BLINK_TIMER_CLOCK_ms, mode=t1.PERIODIC, callback=toggle_led)

print('\r\nESP32 Ready to accept Commands\r\n')

while True:
    print('waiting for connection')
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    # response = web_page()
    # conn.send(response)
    response = 'test'
    conn.send(response)
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
        Command=input('')
        if Command == 'T':
            if led_blink_active_flag == 1:
                print("TLED blinking paused \r\n")
            else:
                print("TLED blinking resumed \r\n")
            led_blink_active_flag ^= 1
        elif Command == 'A':
            print('AReceived the A command\r\n')
            #timer_period = LED_BLINK_TIMER_CLOCK_ms
            #t1.init(period=timer_period,callback=toggle_led)
            dc_motorL.forward(100) # motor is running
            dc_motorR.forward(100)
            #print("AMove Forward")
        elif Command == 'B':
            print('BReceived the B command\r\n')
            #timer_period=timer_period-100
            #t1.init(period=timer_period,callback=toggle_led)
            #if timer_period <= 200:
             #   timer_period = 200
            dc_motorL.backwards(100) # the motor turns in the opposite direction
            dc_motorR.backwards(100) # the motor turns in the opposite direction
            #print("BMove Backward")
        elif Command == 'C':
            print('CReceived the C command\r\n')
            timer_period = LED_BLINK_TIMER_CLOCK_ms
            t1.init(period=timer_period,callback=toggle_led)
        elif Command == 'D':
            print('DReceived the D command\r\n')
            timer_period=timer_period-100
            t1.init(period=timer_period,callback=toggle_led)
            if timer_period <= 200:
                timer_period = 200
        elif Command == 'E':
            print('EReceived the E command\r\n')
            timer_period = LED_BLINK_TIMER_CLOCK_ms
            t1.init(period=timer_period,callback=toggle_led)
        elif Command == 'F':
            print('FReceived the F command\r\n')
            timer_period=timer_period-100
            t1.init(period=timer_period,callback=toggle_led)
            if timer_period <= 200:
                timer_period = 200
        elif Command == 'G':
            print('GReceived the G command\r\n')
            timer_period = LED_BLINK_TIMER_CLOCK_ms
            t1.init(period=timer_period,callback=toggle_led)
        elif Command == 'H':
            print('HReceived the H command\r\n')
            timer_period=timer_period-100
            t1.init(period=timer_period,callback=toggle_led)
            if timer_period <= 200:
                timer_period = 200
        elif Command == 'I':
            print('IESP32\r\n')
        elif Command == 'J':
            print('JReceived the J command\r\n')
            #timer_period = LED_BLINK_TIMER_CLOCK_ms
            #t1.init(period=timer_period,callback=toggle_led)
            dc_motorL.stop() # stops motor
            dc_motorR.stop() # stops motor
