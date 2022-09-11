from machine import UART, Pin
import time
from UartLoadcell import *
from UartWifi import *
#pc수리센터 wifi
#ssid="ipti2"
#password="pc123456789"
#twosome wifi
#ssid="twosome2"
#password="twosome23uu"
#ssid="jjingos"
#password="wlsrn212"


class pimcsMat():
    
    def __init__(self,uartWifi,uartLoadcell,serial):
        self.uartWifi=uartWifi
        self.uartLoadcell=uartLoadcell
        self.serial=serial
        self.weight=0
        self.temp=0
        self.sendWeight=0
        self.weightLimit=2
        self.crlf="\r\n"
        self.communicateCheckTime=time.time()
        self.run()
        
    def uartCommunication(self,uart,command,sleepTime):
        recv=bytes()
        uart.write(command)
        time.sleep(sleepTime)
    
        while uart.any()>0:
            recv+=uart.read(1)
        return recv
    
    
    def apConnect(self):
        self.uartWifi.apConnect()
            
    def sendDataByTCP(self,sendData,Mode="TCP"):
        isSucces=self.uartWifi.sendDataByTCP(sendData,Mode)
        
        if isSucces==False:
            self.apConnect()
            print("보내기 실패")
            self.sendDataByTCP(sendData)
            

    def getLoadcellData(self):
        return self.uartLoadcell.getLoadcellData()

    
    def chDataForm(self,weight,header):
        padding = "00000"
        strWeight=str(weight)
        
        if weight < 0 or weight > 9999:
            header="ER"
            result=header+','+self.serial+','+padding
        else:
            result=header+','+self.serial+','+padding[:-len(strWeight)]+strWeight
        return result
        
        
    #10분에 한번 보내는 
    def communicateCheck(self):
        elapsedTime=time.time()-self.communicateCheckTime
        if elapsedTime >60:
            chData=self.chDataForm(self.sendWeight,"IN")
            self.sendDataByTCP(chData)

    
    
    def run(self):
        while True:
            self.communicateCheck()
            
            weight=int(input("무게 입력:"))
            #보낸 데이터와 현재 무게가 2g이상 차이나면 검사
            if abs(self.sendWeight-int(weight))>self.weightLimit:
                #무게값이 안정되기 위한 여유 시간
                time.sleep(3)
                #검사한 무게값과 현재 무게값이 같으면 데이터가 안정되었다고 판별
                getLoadcellTestData=int(input("무게값입력:"))
                if abs(weight-getLoadcellTestData)<=2:
                #if abs(weight-self.getLoadcellData())<=2:
                    #socket서버에 맞는 dataFormat으로 변경 후 전송
                    chData=self.chDataForm(weight,"CH")
                    self.sendDataByTCP(chData)
                    #검사한 무게값을 보낸 데이터에 대
                    self.sendWeight=weight
                else:
                    continue
        
        
connectId=0
addr="172.30.1.86"
port=9999
serial="WS01E210001"

ssid="twosome2"
password="twosome2388"
uartLoadcell = UartLoadcell(0, 4800, bits=8, parity=None, stop=1)
uartWifi = UartWifi(1,115200,ssid,password,connectId,addr,port)


pimcsMat=pimcsMat(uartWifi,uartLoadcell,serial)
