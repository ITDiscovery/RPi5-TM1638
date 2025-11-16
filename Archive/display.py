#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import tm1637

# Initialize the display (GND, VCC=3.3V, Example Pins are DIO-21 and CLK20)
# Do not use GPIO5 and GPIO6 for a display.
Display1 = tm1637.TM1637(CLK=13, DIO=12, brightness=1.0)
Display2 = tm1637.TM1637(CLK=19, DIO=16, brightness=1.0)
Display3 = tm1637.TM1637(CLK=26, DIO=20, brightness=1.0)
Display4 = tm1637.TM1637(CLK=21, DIO=22, brightness=1.0)

# Display.ShowDoublepoint(True)
Display1.SetBrightness(0.1)
Display2.SetBrightness(0.1)
Display3.SetBrightness(0.1)
Display4.SetBrightness(0.1)

itime = 1000
while (itime<10000):
  digits=[int(tmp) for tmp in str(itime)]
  Display1.Show(digits)
  Display2.Show(digits)
  Display3.Show(digits)
  Display4.Show(digits)
  sleep(.05)
  itime=itime+1

Display1.cleanup()
Display2.cleanup()
Display3.cleanup()
Display4.cleanup()
