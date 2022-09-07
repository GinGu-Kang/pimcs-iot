from machine import UART, Pin
import time


#atcommand AT+CIFSR : local ip address
#AT+CWJAP="jjingos","wlsrn212"
#AT+CIPSTART="TCP","naver.com",80
#AT+CIPMUX=1
#AT+CIPSTART=0,"TCP","172.20.10.3",9996
#AT+CIPSEND=0,76   
def apConnect(uart,ssid,password):
    rxData=bytes()
    connectCommand=bytes()
    
    connectCommand='AT+CWJAP="'+ssid+'","'+password+'"'
    rxData=uartSerialRxMonitor(uart,connectCommand,5)
    print(rxData)


def uartSerialRxMonitor(uart,command,sleepTime):
    #command+='\r\n'
    uart.write(command)
    time.sleep(sleepTime)
    
    recv=bytes()
    
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    erase_len=len(command)
    res = res[erase_len:]
    return res
def uartRecv(uart,sleepTime):
    time.sleep(sleepTime)
    
    recv=bytes()
    
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    return res


ssid="jjingos"
password="wlsrn212"
uart0 = UART(1,115200)

#




while True:
    sendCommand=bytes()
    #sendCommand="AT+CWJAP='"+ssid+"','"+password+"'"
    sendCommand=input("입력: ")

    if sendCommand=='apConnect':
        apConnect(uart0,ssid,password)
    elif sendCommand=='q':
        break
    elif sendCommand=='r':
        res=uartRecv(uart0,1)
        print(res)
    else:
        response=uartSerialRxMonitor(uart0,sendCommand,2)
        print(response)
        
    


