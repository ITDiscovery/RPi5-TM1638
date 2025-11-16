from rpi_TM1638 import TMBoards
from time import sleep
DIO=19
CLK=13
STB=26

TM=TMBoards(DIO,CLK,STB,0)
TM.clearDisplay()
LampDict = {0x01,0x03,0x05,0x07,0x09,0x0b,0x0d,0x0f}


while True:
  for y in range(7):
     TM.turnOn(y)
     for x in LampDict:
       TM.sendCommand(0x44,0)
       TM.sendData(x,1,0)
       TM.segments[4]="{:02}".format(x)
       sleep(.01)
       TM.sendData(x,2,0)
       TM.segments[4]="{:02}".format(x+1)
       sleep(.01)
       TM.sendData(x,3,0) #I think turns on both
       sleep(.01)
       TM.sendData(x,0,0)
       sleep(.01)
