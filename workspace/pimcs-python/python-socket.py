import socket

import time
import sys
import math
import asyncio
import threading

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
        
else:
    from emulated_hx711 import HX711

class Mat():
    
    def __init__(self,serial_number,data_pin, clock_pin,ip,referenceUnit,sleep, weight=0.99, ERROR=2,WEIGHT_LENGTH=5):
        self.ERROR = ERROR
        self.ip = ip
        self.sleep= sleep
        self.weight = weight
        self.serial_number = serial_number
        self.pre_weight = 0
        self.hx = HX711(data_pin, clock_pin )
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(referenceUnit)
        self.hx.reset()
        self.hx.tare()
        
    def run(self):
        while True:
            
            val = int(self.hx.get_weight(5))* self.weight
            if abs(int(val)-self.pre_weight) > self.ERROR:
                self.send(int(val))
            self.hx.power_down()
            self.hx.power_up()
            self.pre_weight = int(val)
            print(self.serial_number, int(val))
            time.sleep(self.sleep)
        #return int(val)
    
    def send(self,val):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip,9999))
        sock.sendall(f"CH,{self.serial_number},{self.setPadding(val)}".encode())
        sock.close()
        print(f"{self.serial_number},send")
    def setPadding(self,weight):
        result = ""
        for i in range(5 - len(f"{weight}")):
            result = result + "0"
        
        return result + f"{weight}"
    
    
def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
        sys.exit()
        


mat1 = Mat(ip="172.20.10.3",serial_number="WS01E210019",data_pin=16,clock_pin=20,referenceUnit=395, sleep=3)
mat2 = Mat(ip="172.20.10.3",serial_number="WS01E210017",data_pin=19,clock_pin=26,referenceUnit=395, sleep=3)
mat3 = Mat(ip="172.20.10.3",serial_number="WS01E210018",data_pin=2,clock_pin=3,referenceUnit=395, weight=3.84615385, sleep=3)

t1=threading.Thread(target=mat1.run)
t2=threading.Thread(target=mat2.run)
t3=threading.Thread(target=mat3.run)
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
time.sleep(1)
t1.start()
time.sleep(1)
t2.start()
time.sleep(1)
t3.start()