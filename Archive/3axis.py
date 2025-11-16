#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to ControlEverything.com for initial code
# https://github.com/massixone/mma8451 also a good source

import time
import datetime
import smbus
import tm1637

# Initialize the display (GND, VCC=3.3V, Example Pins are DIO-21 and CLK20)
# Do not use GPIO5 and GPIO6 for a display.
Display1 = tm1637.TM1637(CLK=13, DIO=12, brightness=1.0)
Display2 = tm1637.TM1637(CLK=19, DIO=16, brightness=1.0)
Display3 = tm1637.TM1637(CLK=26, DIO=20, brightness=1.0)
Display4 = tm1637.TM1637(CLK=21, DIO=22, brightness=1.0)

# Set Brightness and Doublepoint
Display1.SetBrightness(0.1)
Display2.SetBrightness(0.1)
Display3.SetBrightness(0.1)
Display4.SetBrightness(0.1)
Display1.Clear
Display2.Clear
Display3.Clear
Display4.Clear

# Initialize the Accelerometer - open I2C Bus and send to register 0x2A
# a Standby and then a "Start", then a Set range to +/- 2g via register 0x0E
bus = smbus.SMBus(1)
acceladdr = 0x1D  #29 - use CLI command "i2cdetect -y 1"
bus.write_byte_data(acceladdr, 0x2A, 0x00)
bus.write_byte_data(acceladdr, 0x2A, 0x01)
# Set for 2G
bus.write_byte_data(acceladdr, 0x0E, 0x00)
# Set or 4G
#bus.write_byte_data(acceladdr, 0x0E, 0x00)

# Setup Portrain/Landscape detection
bus.write_byte_data(acceladdr, 0x11,0x40)

# Wait for setup
time.sleep(0.5)

while True:
    # Read the data back from register 0x00, 7 byte block
    # Status register, X-Axis MSB, X-Axis LSB,
    # Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    acceldata = bus.read_i2c_block_data(0x1D, 0x00, 7)
    # Display1 is X data (Roll)
    dispdata = (acceldata[1]*256 + acceldata[2])/16
    if dispdata > 2047:
        dispdata -= 4096
    if dispdata > 999:
        dispdata = 999
    if dispdata < -999:
        dispdata = -999
    Display1.Show2Comp(dispdata)
    # Display 2 is Y data (Pitch)
    dispdata = (acceldata[3]*256 + acceldata[4])/16
    if dispdata > 2047:
        dispdata -= 4096
    if dispdata > 999:
        dispdata = 999
    if dispdata < -999:
        dispdata = -999
    Display2.Show2Comp(dispdata)
    # Dusokat 3 is Z data (Yaw)
    dispdata = (acceldata[5]*256 + acceldata[6])/16
    if dispdata > 2047:
        dispdata -= 4096
    if dispdata > 999:
        dispdata = 999
    if dispdata < -999:
        dispdata = -999
    Display3.Show2Comp(dispdata)
    #Read Portrait/Landscape Status
    pl_status = bus.read_byte_data(0x1D, 0x10)
    #PL Status Bit 6=Lockout, Bit 2 and 1 Pu,Pd,Lr,LL and Bit 0 Back/Front 
    print(bin(pl_status),"/n")
    if(pl_status > 64):
        Display4.Show([24,24,24,24])
    else:
        Display4.Show1(1,16)
        #Get Bit's 2 and 3
        pl_orien = pl_status & 0x06
        if (pl_orien == 0):
            Display4.Show1(2,27)
            Display4.Show1(3,28)
        if (pl_orien == 2):
            Display4.Show1(2,27)
            Display4.Show1(3,13)
        if (pl_orien == 4):
            Display4.Show1(2,25)
            Display4.Show1(3,29)
        if (pl_orien == 6):
            Display4.Show1(2,25)
            Display4.Show1(3,25)
        pl_orien = pl_status & 0x01
        if (pl_orien):
            Display4.Show1(0,11)
        else:
            Display4.Show1(0,15)
    time.sleep(0.5)
