from machine import Pin, PWM
import utime

class ServoMotor:
    def __init__(self, pin_number, min_duty, max_duty):
        self.pin = Pin(pin_number)
        self.pwm = PWM(self.pin)
        self.factor = 180/(max_duty-min_duty)
        self.offset = min_duty
        self.pwm.freq(50)


    def set_duty_cycle(self, duty):
        self.pwm.duty_u16(duty)
        print(duty)
    def set_angle(self, angle):
        duty = angle / self.factor + self.offset
        self.set_duty_cycle(int(duty))