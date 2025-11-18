import time
import sys
import os

# Ensure we can find the library
from RPi5_TM1638 import TMBoards

# Pin definitions (must match your hardware)
DIO = 19
CLK = 13
STB_PINS = (26, 6, 5)

print("Initializing TM1638...")
# Initialize board
TM = TMBoards(DIO, CLK, STB_PINS, 3)

print("Starting RAW Key Test.")
print("Using new TM.read_keys_raw(0) method.")
print("Press Ctrl+C to exit.")
print("-" * 40)

try:
    while True:
        # --- NEW CLEAN READ SEQUENCE ---
        # This single call performs the manual STB control, 
        # sends 0x42, waits 1ms, reads, and raises STB.
        keys = TM.read_keys_raw(0)
        
        # --- OUTPUT ---
        # Print the raw data. 
        print(f"Raw Data: {keys}   ", end='\r')
        
        # Small delay to save CPU
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\nTest stopped.")
    TM.clearDisplay()
