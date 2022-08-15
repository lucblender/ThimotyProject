from machine import Pin
import utime


class StepperMotor:
    def __init__(self, step, dir, ms1, ms2, ms3, enable, sw0, sw1, microstep, length):        
        self.step = Pin(step, Pin.OUT)
        self.dir = Pin(dir, Pin.OUT)
        self.ms1 = Pin(ms1, Pin.OUT)
        self.ms2 = Pin(ms2, Pin.OUT)
        self.ms3 = Pin(ms3, Pin.OUT)
        self.enable = Pin(enable, Pin.OUT)
        self.sw0 = Pin(sw0, Pin.IN, Pin.PULL_UP)
        self.sw1 = Pin(sw1, Pin.IN, Pin.PULL_UP)
        self.set_microstep(microstep)
        self.length = length
        self.step_length = 0
        self.enable(1)
        self.step(0)
        self.initialized = False
    
    def set_microstep(self, microstep):
        self.microstep = microstep
        if self.microstep == 1:
            self.ms1.value(0)
            self.ms2.value(0)
            self.ms3.value(0)
        elif self.microstep == 2:
            self.ms1.value(1)
            self.ms2.value(0)
            self.ms3.value(0)
        elif self.microstep == 4:
            self.ms1.value(1)
            self.ms2.value(0)
            self.ms3.value(1)
        elif self.microstep == 8:
            self.ms1.value(1)
            self.ms2.value(1)
            self.ms3.value(0)
        elif self.microstep == 16:
            self.ms1.value(1)
            self.ms2.value(1)
            self.ms3.value(1)
        elif self.microstep == 32:
            self.ms1.value(0)
            self.ms2.value(1)
            self.ms3.value(0)
            
    def init_position(self):
        last_microstep = self.microstep
        step = 0
        self.set_microstep(1)
        self.enable(0)
        self.dir.value(0)
        while(self.sw0.value() == 1):
            self.step.value(1)
            utime.sleep(0.0001)
            self.step.value(0)
            utime.sleep(0.002)  
        self.dir.value(1)
        while(self.sw1.value() == 1):
            self.step.value(1)
            utime.sleep(0.0001)
            self.step.value(0)
            utime.sleep(0.002)
            step += 1
        print("Number of step in cursor =", step)
        self.step_length = step
        self.dir.value(0)
        for i in range(0, int(step/2)):
            self.step.value(1)
            utime.sleep(0.0001)
            self.step.value(0)
            utime.sleep(0.001)
        self.enable(1)        
        self.set_microstep(last_microstep)
        
        self.initialized = True
        
    def do_step(self, factor, stepNumber, direction):
        
        self.enable(0)
        self.dir.value(direction)
        for i in range(0,stepNumber):
            if direction == 0:
                if self.sw0.value() == 0:
                    break
            elif direction == 1:
                if self.sw1.value() == 0:
                    break
            self.step.value(1)
            utime.sleep(0.0001)
            self.step.value(0)
            utime.sleep(0.001*factor)        
        self.enable(1)
        
    def do_lenght(self, factor, length, direction):
        if self.initialized == False:
           self.init_position()
        stepNumber = int((length/self.length)*self.step_length)
        print(stepNumber)
        self.enable(0)
        self.dir.value(direction)
        for i in range(0,stepNumber*self.microstep):
            if direction == 0:
                if self.sw0.value() == 0:
                    break
            elif direction == 1:
                if self.sw1.value() == 0:
                    break
            self.step.value(1)
            utime.sleep(0.0001)
            self.step.value(0)
            utime.sleep(0.001*factor)        
        self.enable(1)
        
    #time in s lenght in mm
    def do_lenght_time(self, time, length, direction):
        if self.initialized == False:
           self.init_position()
        stepNumber = int((length/self.length)*self.step_length)        
        print(stepNumber)
        local_microstep = 1
        step_sleep = time/stepNumber
        while(step_sleep > 0.002 and local_microstep < 32):
            stepNumber *= 2
            local_microstep *= 2                
            step_sleep = time/stepNumber
        step_sleep*=1000
        if local_microstep == 1 and step_sleep<1:
            step_sleep = 1
            print("*warning* expected speed to fast, passed from", time, "s to", step_sleep*0.001*stepNumber, "s")
        print(step_sleep)
        print(local_microstep)
        self.set_microstep(local_microstep)
        self.do_lenght(step_sleep, length, direction)
        
    
            

