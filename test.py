#!/usr/bin/env python3

"""
A "Blink Test" for the full 8-digit display.
It shows '88888888' for 1 second, then blanks for 1 second,
and repeats until you press Ctrl+C.
"""

import time
import sys
from gpiod_TM1638 import TMBoards

# --- Configuration ---
# Your GPIO settings
DIO = 19
CLK = 13
STB = 26
# ---------------------

try:
    # Use 'with' to auto-initialize and clean up the GPIO pins
    with TMBoards(DIO, CLK, STB, brightness=2, gpio_chip_name="gpiochip0") as tm:
        
        print("Test started. Displaying '88888888' blink.")
        print("Press Ctrl+C to exit.")
        
        # Clear all segments and LEDs to start
        tm.clearDisplay()
        
        while True:
            # 1. Turn on all segments (display '8' on all digits)
            tm.segments[0] = '88888888'
            time.sleep(1)
            
            # 2. Turn off all segments (display blanks)
            tm.segments[0] = '        ' # 8 spaces
            time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print("\nExiting test. Display will be cleared.")
    # The 'with' block exiting will automatically call tm.close()
    # and clean up the pins.
except Exception as e:
    print(f"\nAn error occurred: {e}")
    sys.exit(1)