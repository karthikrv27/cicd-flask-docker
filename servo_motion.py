from machine import Pin, PWM
import time

# Create PWM object on pin 19
servo = PWM(Pin(19), freq=50)
pins = Pin(33, Pin.IN)

def calculate_angle(motion):
    if motion == 1:
        return 180
    return 0

def set_angle(angle):
    duty = int((angle / 180) * 75 + 40)
    servo.duty(duty)

while True:
    motion = pins.value()

    angle = calculate_angle(motion)

    set_angle(angle)

    time.sleep(2)