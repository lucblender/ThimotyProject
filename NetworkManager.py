import network
import socket
from time import sleep
import machine
from machine import Pin
from StepperMotor import StepperMotor

led = Pin("LED", Pin.OUT)
 
ssid = 'ssid'
password = 'password'
class NetworkManager:
    
    def __init__(self, local_stepper):
        self.local_stepper = local_stepper
        pass
    
    def connect(self):
        #Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')        
        led.value(1)
        return ip

    def webpage(self, lenght, step_number):
        #Template HTML
        html = f"""
<!DOCTYPE html>
<html>
<body>

<p>The cursor measure {lenght}mm. This lenght include {step_number} motor steps.</p>


<form action="./initialize">
<input type="submit" value="Initialize the cursor" />
</form>


<form action="/lenghtTime" method="GET">
    <p>Enter the lenght in mm, the time in s and the direction (0 or 1) </p>
    <input type="number" step="0.01" name="lenght" placeholder="lenght [mm]" required>
    <input type="number" step="0.01" name="time" placeholder="time [s]" required>
    <input type="number" step="1" name="direction" placeholder="direction (0,1)" required>
    <button type="submit">Submit</button>  
</form>

                """
        return str(html)

    def open_socket(self, ip):
        # Open a socket
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        print(connection)
        return connection

    def serve(self, connection):
        #Start a web server
        state = 'OFF'
        temperature = 0
        while True:
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            try:
                request = request.split()[1]
            except IndexError:
                pass
            if request == '/lighton?':
                print("lighton")
                led.value(1)
                state = 'ON'
            elif request =='/lightoff?':
                print("lightoff")
                led.value(0)
                state = 'OFF'
            elif "initialize" in request:                
                self.local_stepper.init_position()
            elif "lenghtTime" in request:                
                print(request)
                lenght = self.get_param_from_url(request, "lenght")
                time = self.get_param_from_url(request, "time")
                direction = self.get_param_from_url(request, "direction")
                try:
                    lenght = float(lenght)
                    time = float(time)
                    direction = int(direction)
                except:
                    print("Parameters wern't correct datatype")
                print(lenght, time, direction)
                    
                self.local_stepper.do_lenght_time(time, lenght, direction)
            html = self.webpage(self.local_stepper.length, self.local_stepper.step_length)
            client.send(html)
            client.close()

    def get_param_from_url(self, url, param_name):
        try:
            to_return = [i.split("=")[-1] for i in url.split("?", 1)[-1].split("&") if i.startswith(param_name + "=")][0]
        except:
            to_return = ""
        return to_return
