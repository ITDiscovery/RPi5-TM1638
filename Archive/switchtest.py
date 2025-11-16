from time import sleep
from rpi_TM1638 import TMBoards

# my GPIO settings
# (one TM1638 board connected to GPIO19 for dataIO, GPIO13 for Clock, and GPIO26
 for the STB)
DIO = 19
CLK = 13
STB = 26,6
# STB = 26,6,5   # in case you have thre TM1638 boards, connected to GPIO26, GPI
O6, and GPIO5

# initialeze TM1638
TM = TMBoards(DIO, CLK, STB, 2)

TM.turnOn(3)
TM.clearDisplay()

LampDict = {0x01,0x03,0x05,0x07,0x09,0x0b,0x0d,0x0f}
KeyDict = {}
KeyDict[1] = [4,0,0,0]
KeyDict[2] = [64,0,0,0]
KeyDict[3] = [0,4,0,0]
KeyDict[4] = [0,64,0,0]
KeyDict[5] = [0,0,4,0]
KeyDict[6] = [0,0,64,0]
KeyDict[7] = [0,0,0,4]
KeyDict[8] = [0,0,0,64]
KeyDict[9] = [2,0,0,0]
KeyDict[10] = [32,0,0,0]
KeyDict[11] = [0,2,0,0]
KeyDict[12] = [0,32,0,0]
KeyDict[13] = [0,0,2,0]
KeyDict[14] = [0,0,32,0]
KeyDict[15] = [0,0,0,2]
KeyDict[16] = [0,0,0,32]
KeyDict[17] = [1,0,0,0]
KeyDict[18] = [16,0,0,0]
KeyDict[19] = [0,1,0,0]
KeyDict[20] = [0,16,0,0]
KeyDict[21] = [0,0,1,0]
KeyDict[22] = [0,0,16,0]
KeyDict[23] = [0,0,0,1]
KeyDict[24] = [0,0,0,16]

while True:
  for y in range(99):
    sleep(.05)
    TM.sendCommand(0x42,0)
    keyval = TM.getData(0)
    keynum = 0
    if (keyval != [0,0,0,0]):
      for x in KeyDict:
        if (KeyDict[x] == keyval):
          keynum=x
      TM.segments[4]="{:02}".format(keynum)
      print("0:",keyval)
    sleep(.05)
    TM.sendCommand(0x42,1)
    keyval = TM.getData(1)
    keynum = 0
    if (keyval != [0,0,0,0]):
       for x in KeyDict:
          if (KeyDict[x] == keyval):
             keynum=x
       TM.segments[4]="{:02}".format(keynum+24)
       print("0:",keyval)
    TM.segments[2]="{:02}".format(y)
