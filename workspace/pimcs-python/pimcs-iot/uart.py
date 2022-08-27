from machine import UART
import machine
import _thread
import time
uart = UART(0,115200)
ssid = "turningpoint_jeon"
pw = "tp47900520"

print('UART Serial')
print('>', end='')

def uartSerialRxMonitor(command):
    recv=bytes()
    while uart.any()>0:
        print(uart.any())
        recv+=uart.read(1)
        #print(recv.decode('utf-8'))
    res=recv.decode('utf-8')
    erase_len=len(command)+5
    res = res[erase_len:]
    return res

while True:
    send=input("Please enter the command\n>")
    if send=='q':
        break
    uart.write(send+'\r\n')
    time.sleep(1)
    res=uartSerialRxMonitor(send)
    print(res)

