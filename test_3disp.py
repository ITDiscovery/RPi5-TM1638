#!/usr/bin/env python3

"""
A "Blink Test" for 3 chained TM1638 displays.
It shows all '8's across all 24 segments, then blanks,
and repeats until you press Ctrl+C.
"""

import time
import sys
from gpiod_TM1638 import TMBoards

# --- Configuration ---
# DIO and CLK are shared (wired in parallel) to all boards
DIO = 19
CLK = 13

# STB (Strobe) must be a unique pin for EACH board.
# !!! EDIT THIS TUPLE to match your 3 STB pins !!!
STB = (26, 6, 5)  # (STB_PIN_BOARD_1, STB_PIN_BOARD_2, STB_PIN_BOARD_3)
# ---------------------

try:
    # We pass the tuple of STB pins to the constructor
    with TMBoards(DIO, CLK, STB, brightness=2, gpio_chip_name="gpiochip0") as tm:
        
        print(f"Test started for {tm.nbBoards} displays.")
        print("Displaying all '8's plus decimal point blink test.")
        print("Press Ctrl+C to exit.")
        
        # Clear all segments and LEDs to start
        tm.clearDisplay()
        
        # We now have 3 boards * 8 segments = 24 segments
        all_eights = '8.' * 24
        all_blanks = ' ' * 24
        
        while True:
            # 1. Turn on all segments on all 3 boards
            tm.segments[0] = all_eights
            time.sleep(1)
            
            # 2. Turn off all segments
            tm.segments[0] = all_blanks
            time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print("\nExiting test. Display will be cleared.")
    # The 'with' block exiting will automatically call tm.close()
    # and clean up the pins.
except Exception as e:
    print(f"\nAn error occurred: {e}")
    sys.exit(1)
