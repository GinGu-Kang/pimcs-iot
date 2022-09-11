from machine import UART, Pin
import time


class UartLoadcell(UART):
    
        
    def getLoadcellData(self):
        command="Q\r\n"
        result=self.uartCommunication(command,1)

        
        if len(result)==9:
            return int(result[1:6])
        else:
            return self.getLoadcellData()
        
    def uartCommunication(self,command,sleepTime):
        recv=bytes()
        self.write(command)
        time.sleep(sleepTime)
        while self.any()>0:
            recv+=self.read(1)
        return recv


