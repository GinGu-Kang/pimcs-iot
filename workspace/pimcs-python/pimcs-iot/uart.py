from machine import UART,Pin
import machine
import time


uart = UART(0, baudrate=9600,timeout=10)
uart.init(9600, bits=8, parity=None, stop=1)
time.sleep(1)
uart.write('AT')
print(uart.read())


