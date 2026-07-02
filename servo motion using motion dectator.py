from machine import Pin, PWM
import time

# Create PWM object on pin 19
servo = PWM(Pin(19), freq=50)   # 50Hz for servo
pins=Pin(33,Pin.IN)

def set_angle(angle):
    duty = int((angle / 180) * 75 + 40)  # duty range for ESP32
    servo.duty(duty)

while True:
   # angle = int(input("Enter angle (0 to 180): "))
    motion=pins.value()
    time.sleep(2)
    if motion ==1:
        angle=180
        set_angle(angle)
    else:
        angle=0
        set_angle(angle)
time.sleep(2)
        
