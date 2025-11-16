#!/usr/bin/env python3

"""
A font test for the gpiod-TM1638 library.
It iterates through all available characters in Font.py
and displays them on the first 6 segments (0-5) of the first board.
"""

import time
import sys
from RPi5_TM1638 import TMBoards
from RPi5_TM1638.Font import FONT  # Import the font dictionary

# --- Configuration ---
# Your proven hardware setup
DIO = 19
CLK = 13
STB = (26, 6, 5)  # (Board 0, Board 1, Board 2)
# ---------------------

# Get all available characters from the FONT dictionary
# We'll sort them by their ASCII value
all_chars = sorted(FONT.keys(), key=ord)

# We will only use the first 6 segments, as requested
DISPLAY_SIZE = 6

try:
    # We initialize all 3 boards, but will only write to the first 6 segments
    with TMBoards(DIO, CLK, STB, brightness=2, gpio_chip_name="gpiochip0") as tm:
        
        print(f"Test started for {tm.nbBoards} displays.")
        print(f"Showing all characters, {DISPLAY_SIZE} at a time, on segments 0-5.")
        print("Press Ctrl+C to exit.")
        
        # Clear all displays to start
        tm.clearDisplay()
        
        while True:
            # Loop through the characters in chunks of 6
            for i in range(0, len(all_chars), DISPLAY_SIZE):
                # Get a 6-character chunk
                chunk = all_chars[i:i + DISPLAY_SIZE]
                
                # Join the characters into a string
                display_string = "".join(chunk)
                
                # Pad the string with spaces to fill all 6 segments
                # This clears the display on the last (partial) chunk
                display_string = display_string.ljust(DISPLAY_SIZE, ' ')
                
                # Print to console and send to the display
                print(f"Displaying: [{display_string}]")
                
                # tm.segments[0] writes to the first board, starting at segment 0
                tm.segments[0] = display_string
                
                # Wait for the user to press Enter in the console
                input("Press Enter to continue to the next set...")

except (KeyboardInterrupt, SystemExit):
    print("\nExiting test. Display will be cleared.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    sys.exit(1)
