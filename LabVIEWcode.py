from machine import Pin, Timer, PWM   
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

# Straight run from (0,0)
#dc_motorL.forward(100)
#sleep(10)
#dc_motorR.backward(100)
#sleep(10)

print('\r\nESP32 Ready to accept Commands\r\n')

try:
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
            dc_motorL.forward(100)
            sleep(10)
            dc_motorL.backward(100)
            sleep(10)
            # dc_motorL.stop()
        elif Command == 'B':
            print('BReceived the B command\r\n')
            #timer_period=timer_period-100
            #t1.init(period=timer_period,callback=toggle_led)
            #if timer_period <= 200:
             #   timer_period = 200
            dc_motorL.backward(100) # the motor turns in the opposite direction
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
            
except:
    t1.deinit()
    pass
