from machine import UART, Pin
import time

class PimcsMat:
    
    def __init__(self,uartWifi,uartModbus,ssid,password,connectId,addr,port):
        self.uartWifi=uartWifi
        self.uartModbus=uartModbus
        self.ssid=ssid
        self.password=password
        self.addr=addr
        self.port=port
        self.connectId=connectId
        self.run()
        
    def sendDataByTCP(self,sendData,Mode="TCP"):
        command="AT+CIPMUX=1"
        res=uartCommunication(self.uartWifi,command,1)
        print(res)    
        command='AT+CIPSTART='+str(self.connectId)+',"'+Mode+'","'+self.addr+'",'+str(self.port)
        res=uartCommunication(self.uartWifi,command,0.1)
        print(res)
        #보낼데이터 길이
        command="AT+CIPSEND=0,"+str((len(sendData)+4))
        res=uartCommunication(self.uartWifi,command,0.1)
        print(res)
        #데이터 전
        command=sendData
        res=uartCommunication(self.uartWifi,command,0.1)
        print(res)
        command="AT+CIPCLOSE"
        res=uartCommunication(self.uartWifi,command,0.1)
        print(res)
        
    def apConnect(self):
        rxData=bytes()
        connectCommand=bytes()
        
        connectCommand='AT+CWJAP="'+self.ssid+'","'+self.password+'"'
        rxData=uartSerialRxMonitor(self.uartWifi,connectCommand,5)
        print(rxData)
        
    def getModbusData:(self)
        command="Q"
        return uartSerialRxMonitor(self.uartModbus,command,1)
    
    def uartCommunication(self,uart,command,sleepTime):
        command+='\r\n'
        uart.write(command)
        time.sleep(sleepTime)
        recv=bytes()
        while uart.any()>0:
            recv+=uart.read(1)
        res=recv.decode('utf-8')
        erase_len=len(command)
        res = res[erase_len:]
        return res
    
    def run(self):
        self.apConnect()
        while True:
            weight=getModbusData()
            sendData=""
            print(weight)
            #보낸데이터(sendData)와 현재 데이터가 2g이상 차이나면 임시저장소에 저장하고 3초기다림
            #현재 데이터와 임시 저장소의 데이터가 같으면 전송 다르면 임시 저장소에 현재 데이터를 집어 넣고 보낸데이터(sendData)와 비교하고 2g이상 차이안나면 데이터 전송 X
            #2g이상 차이나면 다시 3초 기다림 이후 현재데이터와 임시 데이터가 같으면 전송 아니면 다시 반복
            if ""=="":
                sendDataByTCP(sendData):
                    
        
    

if __main__ == __name__:
    ssid="jjingos"
    password="wlsrn212"
    connectId=0
    addr="172.20.10.3"
    port=9994
    uartWifi = UART(1,115200)
    uartModbus = UART(0, 4800, bits=8, parity=None, stop=1)
    pimcsMat = PimcsMat(uartWifi,uartModbus,ssid,password,addr,port)

