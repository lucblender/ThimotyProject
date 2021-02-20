from StepperMotor import StepperMotor
from ServoMotor import ServoMotor
from machine import Pin
import utime

led = Pin(25,Pin.OUT)
led.high()
utime.sleep(0.1)   
led.low()
utime.sleep(0.1)   
led.high()

stepper = StepperMotor(1, 0, 3, 4, 5, 6, 16, 17, 1, 200)
servoA = ServoMotor(20, 1600, 8200)
servoB = ServoMotor(26, 1600, 8200)

stepper.init_position()
