#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import pytz
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
Display1.ShowDoublepoint(True)
Display2.ShowDoublepoint(True)
Display3.ShowDoublepoint(True)
Display4.ShowDoublepoint(True)

while True:
    utc_now = pytz.utc.localize(datetime.datetime.now())
    cst_now = utc_now.astimezone(pytz.timezone("America/Chicago"))
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    zst_now = utc_now.astimezone(pytz.timezone("Europe/Zurich"))
    hour = utc_now.hour
    minute = utc_now.minute
    currenttime = [int(hour/10),hour%10,int(minute/10),minute%10]
    Display2.Show(currenttime)
    hour = pst_now.hour
    currenttime = [int(hour/10),hour%10,int(minute/10),minute%10]
    Display4.Show(currenttime)
    hour = cst_now.hour
    currenttime = [int(hour/10),hour%10,int(minute/10),minute%10]
    Display3.Show(currenttime)
    hour = zst_now.hour
    currenttime = [int(hour/10),hour%10,int(minute/10),minute%10]
    Display1.Show(currenttime)
    time.sleep(1)
