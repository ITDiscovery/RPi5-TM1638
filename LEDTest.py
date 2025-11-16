#!/usr/bin/env python3

"""
A test script for the 16 LEDs (8 bi-color) on a TM1638 board.
This will cycle through Green, Red, and Amber/Yellow.
"""

import time
import sys
from gpiod_TM1638 import TMBoards

# --- Configuration ---
# We still need to define all 3 boards so the
# library initializes correctly.
DIO = 19
CLK = 13
STB = (26, 6, 5) # (Board 1, Board 2, Board 3)
# ---------------------

# LED addresses are the 8 ODD addresses: 1, 3, 5, 7, 9, 11, 13, 15
LED_ADDRESSES = [addr * 2 + 1 for addr in range(8)]

# Data values for colors
GREEN = 1  # Bit 0
RED = 2    # Bit 1
AMBER = 3  # Bit 0 + Bit 1
OFF = 0

try:
    with TMBoards(DIO, CLK, STB, brightness=2, gpio_chip_name="gpiochip0") as tm:
        
        print(f"Test started for {tm.nbBoards} displays.")
        print("Testing 16 LEDs (8 bi-color) on Board 1.")
        print("Press Ctrl+C to exit.")
        
        # Clear all displays to start
        tm.clearDisplay()
        
        while True:
            
            # --- 1. All 8 GREEN LEDs ---
            print("All GREEN")
            for addr in LED_ADDRESSES:
                # We send to TMindex=0 (the first board)
                tm.sendData(addr, GREEN, 0)
            time.sleep(1)

            # --- 2. All 8 RED LEDs ---
            print("All RED")
            for addr in LED_ADDRESSES:
                tm.sendData(addr, RED, 0)
            time.sleep(1)

            # --- 3. All 8 AMBER LEDs ---
            print("All AMBER (Green + Red)")
            for addr in LED_ADDRESSES:
                tm.sendData(addr, AMBER, 0)
            time.sleep(1)
            
            # --- 4. All OFF ---
            print("All OFF")
            for addr in LED_ADDRESSES:
                tm.sendData(addr, OFF, 0)
            time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print("\nExiting test. Display will be cleared.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    sys.exit(1)