#!/usr/bin/env python3

"""
A "Key Discovery" test for the TM1638 boards.
This version uses the manual sendCommand(0x42) and delay
from the working RPi4 switchtest.py.
"""

import time
import sys
from RPi5_TM1638 import TMBoards

# --- Configuration ---
DIO = 19
CLK = 13
STB = (26, 6, 5) # (Board 0, Board 1, Board 2)
# ---------------------

def check_all_keys(tm, board_index):
    """
    Scans one board and returns a list of pressed keys.
    """
    pressed_keys = []
    
    # === This is the new logic ===
    
    # 1. Pull STB low
    tm._setStb(False, board_index)
    
    # 2. Send the "Read Key" command
    tm._setDataMode(0x02, 0x00) # READ_MODE, INCR_ADDR (sends 0x42)
    
    # 3. Get the 4 data bytes (using our new "dumb" getData)
    sw_data = tm.getData(board_index)

    # 4. Pull STB high
    tm._setStb(True, board_index)
    
    # === End new logic ===

    # Check all K1 lines (KS1-8)
    # The original library (MSB-first) had this bit mapping:
    if sw_data[0] & 0x01: pressed_keys.append(f"Board {board_index}, K1, KS1")
    if sw_data[0] & 0x10: pressed_keys.append(f"Board {board_index}, K2, KS1")
    if sw_data[0] & 0x02: pressed_keys.append(f"Board {board_index}, K1, KS2")
    if sw_data[0] & 0x20: pressed_keys.append(f"Board {board_index}, K2, KS2")
    if sw_data[0] & 0x04: pressed_keys.append(f"Board {board_index}, K1, KS3")
    if sw_data[0] & 0x40: pressed_keys.append(f"Board {board_index}, K2, KS3")
    if sw_data[0] & 0x08: pressed_keys.append(f"Board {board_index}, K1, KS4")
    if sw_data[0] & 0x80: pressed_keys.append(f"Board {board_index}, K2, KS4")
    
    if sw_data[1] & 0x01: pressed_keys.append(f"Board {board_index}, K1, KS5")
    if sw_data[1] & 0x10: pressed_keys.append(f"Board {board_index}, K2, KS5")
    # ... and so on ...
    # This logic is based on the original lib's weird mapping,
    # let's just print the raw data.

    return sw_data, pressed_keys

# --- Main Test ---
try:
    with TMBoards(DIO, CLK, STB, brightness=1, gpio_chip_name="gpiochip0") as tm:
        
        print(f"Key test started for {tm.nbBoards} boards.")
        print("Press any key on your DSKY...")
        print("Press Ctrl+C to exit.")
        tm.clearDisplay()
        
        last_data_str = ""

        while True:
            all_data = []
            
            # Check all 3 boards, ONE AT A TIME, with a delay
            for i in range(tm.nbBoards):
                # This logic comes from your working RPi4 script:
                time.sleep(0.05) # 50ms delay
                
                # 1. Pull STB low
                tm._setStb(False, i)
                
                # 2. Send the "Read Key" command
                tm._setDataMode(0x02, 0x00) # READ_MODE, INCR_ADDR (sends 0x42)
                
                # 3. Get the 4 data bytes (using our new "dumb" getData)
                sw_data = tm.getData(i)
                all_data.append(f"B{i}: {sw_data[0]:02x} {sw_data[1]:02x} {sw_data[2]:02x} {sw_data[3]:02x}")

                # 4. Pull STB high
                tm._setStb(True, i)
            
            # Print the raw data if it has changed
            current_data_str = " | ".join(all_data)
            if current_data_str != last_data_str:
                print(current_data_str)
                last_data_str = current_data_str
                
                # Show key press on display
                if current_data_str != "B0: 00 00 00 00 | B1: 00 00 00 00 | B2: 00 00 00 00":
                    tm.segments[0] = "KEY DN"
                else:
                    tm.segments[0] = "        "

except (KeyboardInterrupt, SystemExit):
    print("\nExiting test. Display will be cleared.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    sys.exit(1)
