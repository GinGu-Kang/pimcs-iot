from machine import UART, Pin
import time

#pc수리센터 wifi
#ssid="ipti2"
#password="pc123456789"
#twosome wifi
#ssid="twosome2"
#password="twosome23uu"



class pimcsMat():
    
    def __init__(self,uartWifi,uartLoadcell,ssid,password,connectId,addr,port,serial):
        self.uartWifi=uartWifi
        self.uartLoadcell=uartLoadcell
        self.ssid=ssid
        self.password=password
        self.addr=addr
        self.port=port
        self.connectId=connectId
        self.serial=serial
        self.weight=0
        self.temp=0
        self.sendWeight=0
        self.weightLimit=2
        self.run()

        
    def sendDataByTCP(self,sendData,Mode="TCP"):
        command=bytes()
        command="AT+CIPMUX=1"
        res=self.uartCommunication(self.uartWifi,command,1)
        command='AT+CIPSTART='+str(self.connectId)+',"'+Mode+'","'+self.addr+'",'+str(self.port)
        res=self.uartCommunication(self.uartWifi,command,0.1)
        command="AT+CIPSEND=0,"+str(len(sendData))
        res=self.uartCommunication(self.uartWifi,command,0.1)
        print(res)
        command=sendData
        print(sendData)
        res=self.uartCommunication(self.uartWifi,command,1,1)
        print(res)
        command="AT+CIPCLOSE"
        res=self.uartCommunication(self.uartWifi,command,0.1)
        print(res)
        
    def apConnect(self):
        rxData=bytes()
        connectCommand=bytes()
        eraseSize=0
        
        #보내기전에 와이파이 연결되어있나 확인
        command="AT+CWJAP?"
        eraseWord=""
        eraseSize=len(command)
        response=self.uartCommunication(self.uartWifi,command,2)
        print(res[eraseSize+8:len(command)+8+len(ssid)])
        
        
        connectCommand='AT+CWJAP="'+self.ssid+'","'+self.password+'"'
        rxData=self.uartCommunication(self.uartWifi,connectCommand,5,2)
        print(rxData)
        
    def getLoadcellData(self):
        command="Q\r\n"
        result=self.uartCommunication(self.uartLoadcell,command).decode('utf-8')
        
        if len(result)==9:
            return int(result[1:6])
        else:
            return getLoadcellData()

    
    def chDataForm(self,weight):
        weight="00050"        
        header="CH"
        if weight[0]=='-':
            header="ER"
            result=header+','+self.serial+','+weight
        else:
            result=header+','+self.serial+','+weight
        return result
        
        
    #10분에 한번 보내는 
    def inDataForm(self,weight):
        weight="00050"
        header="IN"
        if weight[0]=='-':
            header="ER"
            result=header+','+self.serial+','+weight
        else:
            result=header+','+self.serial+','+weight
        return result
        
    
    #wirtemode 0, sendmode=1, wificonnectmode=2
    #mode 쓰지말고 decode전 데이터만 보내서 가져온 함수에서 가공하기
    #command 뒤에도 \r\n알아서 붙히기
    def uartCommunication(self,uart,command,sleepTime)
        recv=bytes()
        uart.write(command)
        time.sleep(sleepTime)
    
        while uart.any()>0:
            recv+=uart.read(1)
        return recv
    
    
    def run(self):
        self.apConnect()
        
        '''while True:
            weight=self.getLoadcellData()
            print(weight)
            #양수만 전송
            if weight>0:
                #보낸 데이터와 현재 무게가 2g이상 차이나면 검사
                if abs(self.sendWeight-weight)>weightLimit:
                    #무게값이 안정되기 위한 여유 시간
                    time.sleep(3)
                    #검사한 무게값과 현재 무게값이 같으면 데이터가 안정되었다고 판별
                    if abs(weight-self.getLoadcellData())<=2:
                        #socket서버에 맞는 dataFormat으로 변경 후 전송
                        chData=self.chDataForm(weight)
                        self.sendDataByTCP(chData)
                        print("dataSend:"+chData)
                        #검사한 무게값을 보낸 데이터에 대
                        self.sendWeight=weight
                    else:
                        continue'''
        
        
        
    
uartWifi = UART(1,115200)
uartLoadcell = UART(0, 4800, bits=8, parity=None, stop=1)    
ssid="twosome2"
password="twosome2388"
connectId=0
addr="192.168.219.116"
port=9999
serial="WS01E210001"
pimcsMat=pimcsMat(uartWifi,uartLoadcell,ssid,password,connectId,addr,port,serial)
