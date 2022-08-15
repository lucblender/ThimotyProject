from StepperMotor import StepperMotor
from ServoMotor import ServoMotor
import machine
from machine import Pin
import utime
from NetworkManager import NetworkManager

led = Pin(25,Pin.OUT)
led.high()
utime.sleep(0.1)   
led.low()
utime.sleep(0.1)   
led.high()

stepper = StepperMotor(1, 0, 3, 4, 5, 6, 16, 17, 1, 200)
servoA = ServoMotor(20, 1600, 8200)
servoB = ServoMotor(26, 1600, 8200)

if stepper.sw0.value() == 0 or stepper.sw0.value() == 0:
    print("one of the limit switch was pressed at boot, websever not launched. Software will end to allow programming")
    
else:
    stepper.init_position()
    networkManager = NetworkManager(stepper)

    try:
        ip = networkManager.connect()
        connection  = networkManager.open_socket(ip)
        networkManager.serve(connection)
    except KeyboardInterrupt:
        machine.reset()

