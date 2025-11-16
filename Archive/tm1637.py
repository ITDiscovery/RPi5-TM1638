#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Modified by Peter Nichols at www.itdiscovery.info
# Original Code from Tim Waizenegger in Stuttgardt
# https://github.com/timwaizenegger/raspberrypi-examples
# actor-led-7segment-4numbers/tm1637.py

import math
import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)

# Array for display 0,1,2,3,4,5,6,7,8,9,A,b,C,d,E,F,blank
#                   Top,Up Right,Low Right,Bot,Bot Left,Top Left,Minus
#                   L,o,P,u,r
HexDigits = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F, 
        0x77,0x7C,0x39,0x5E,0x79,0x71,0x00,
        0x01,0x02,0x04,0x08,0x10,0x20,0x21,0x40,
        0x38,0x5C,0x73,0x1C,0x50]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0


class TM1637:
    __doublePoint = False
    __Clkpin = 0
    __Datapin = 0
    __brightness = 1.0  # default to max brightness
    __currentData = [0, 0, 0, 0]

    def __init__(self, CLK, DIO, brightness):
        self.__Clkpin = CLK
        self.__Datapin = DIO
        self.__brightness = brightness
        IO.setup(self.__Clkpin, IO.OUT)
        IO.setup(self.__Datapin, IO.OUT)

    def cleanup(self):
        # Stop updating clock, turn off display, and cleanup GPIO
        self.Clear()
        IO.cleanup()

    def Clear(self):
        b = self.__brightness
        point = self.__doublePoint
        self.__brightness = 0
        self.__doublePoint = False
        data = [0x7F, 0x7F, 0x7F, 0x7F]
        self.Show(data)
        # Restore previous settings:
        self.__brightness = b
        self.__doublePoint = point

    def ShowInt(self, i):
        s = str(i)
        self.Clear()
        for i in range(0, len(s)):
            self.Show1(i, int(s[i]))
            
    def Show2Comp(self,i):
        self.Clear()
        if i < 0:
            self.Show1(0,24)
            s='{:03d}'.format(int(i)*-1)
        else:
            s='{:03d}'.format(int(i))
        for i in range(0,3):
                self.Show1(i+1, int(s[i]))

    def Show(self, data):
        for i in range(0, 4):
            self.__currentData[i] = data[i]

        self.start()
        self.writeByte(ADDR_AUTO)
        self.br()
        self.writeByte(STARTADDR)
        for i in range(0, 4):
            self.writeByte(self.coding(data[i]))
        self.br()
        self.writeByte(0x88 + int(self.__brightness))
        self.stop()

    def Show1(self, DigitNumber, data):
        # Show one Digit (number 0...3)
        if(DigitNumber < 0 or DigitNumber > 3):
            return  # error

        self.__currentData[DigitNumber] = data

        self.start()
        self.writeByte(ADDR_FIXED)
        self.br()
        self.writeByte(STARTADDR | DigitNumber)
        self.writeByte(self.coding(data))
        self.br()
        self.writeByte(0x88 + int(self.__brightness))
        self.stop()

    def SetBrightness(self, percent):
        # Accepts percent brightness from 0 - 1
        max_brightness = 7.0
        brightness = math.ceil(max_brightness * percent)
        if (brightness < 0):
            brightness = 0
        if(self.__brightness != brightness):
            self.__brightness = brightness
            self.Show(self.__currentData)

    def ShowDoublepoint(self, on):
        # Show or hide double point divider
        if(self.__doublePoint != on):
            self.__doublePoint = on
            self.Show(self.__currentData)

    def writeByte(self, data):
        for i in range(0, 8):
            IO.output(self.__Clkpin, IO.LOW)
            if(data & 0x01):
                IO.output(self.__Datapin, IO.HIGH)
            else:
                IO.output(self.__Datapin, IO.LOW)
            data = data >> 1
            IO.output(self.__Clkpin, IO.HIGH)

        # wait for ACK
        IO.output(self.__Clkpin, IO.LOW)
        IO.output(self.__Datapin, IO.HIGH)
        IO.output(self.__Clkpin, IO.HIGH)
        IO.setup(self.__Datapin, IO.IN)

        while(IO.input(self.__Datapin)):
            sleep(0.001)
            if(IO.input(self.__Datapin)):
                IO.setup(self.__Datapin, IO.OUT)
                IO.output(self.__Datapin, IO.LOW)
                IO.setup(self.__Datapin, IO.IN)
        IO.setup(self.__Datapin, IO.OUT)

    def start(self):
        # Send start signal to TM1637"""
        IO.output(self.__Clkpin, IO.HIGH)
        IO.output(self.__Datapin, IO.HIGH)
        IO.output(self.__Datapin, IO.LOW)
        IO.output(self.__Clkpin, IO.LOW)

    def stop(self):
        IO.output(self.__Clkpin, IO.LOW)
        IO.output(self.__Datapin, IO.LOW)
        IO.output(self.__Clkpin, IO.HIGH)
        IO.output(self.__Datapin, IO.HIGH)

    def br(self):
        # terse break
        self.stop()
        self.start()

    def coding(self, data):
        if(self.__doublePoint):
            pointData = 0x80
        else:
            pointData = 0

        if(data == 0x7F):
            data = 0
        else:
            data = HexDigits[data] + pointData
        return data

if __name__ == "__main__":
    # Confirm the display operation
    display = TM1637(CLK=21, DIO=22, brightness=1.0)

    display.Clear()
    print("Displaying all 8's")
    digits = [8,8,8,8]
    display.Show(digits)
    sleep(2)
    print ("Updating one digit at a time:")
    display.Clear()
    display.Show1(0,1)
    sleep(1)
    display.Show1(1,2)
    sleep(1)
    display.Show1(2,3)
    sleep(1)
    display.Show1(3,4)
    sleep(2)
    print("Show 2's compliment - negative\n")
    display.Show2Comp(-987)
    sleep(3)
    print("Show 2's compliment - positive")
    display.Show2Comp(456)
    sleep(3)

    print("Add double point\n")
    display.ShowDoublepoint(True)
    sleep(2)
    print("Brightness Off")
    display.SetBrightness(0)
    sleep(1)
    print("Full Brightness")
    display.SetBrightness(1)
    sleep(1)
    print("30% Brightness")
    display.SetBrightness(0.1)
    sleep(2)
    print("Clearing Display")
    display.Clear()
    display.cleanup()
