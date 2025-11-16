# Pi 5 TM1638 Library (gpiod)

This is a Python 3 library for controlling TM1638-based LED and key modules on a **Raspberry Pi 5** or any other system using the modern `gpiod` v2 library.

This library was ported from the original `rpi-TM1638` (which used the deprecated `RPi.GPIO`) and extensively debugged to solve complex timing and API issues specific to the new `gpiod` v2 interface.

## Features

* Full support for chained TM1638 boards.
* Control for 8-segment displays.
* Control for bi-color (Red/Green) LEDs.
* Reliable key/button scanning.
* Written for Python 3 and the Raspberry Pi 5 (`gpiod` v2 API).

## 1. Prerequisites

This library is built on `gpiod` and requires no `sudo` to run.

**1. Install the `gpiod` library:**
```bash
sudo apt update
sudo apt install python3-gpiod
```

**2. Add Your User to the `gpio` Group:**
You must be a member of the `gpio` group to access the GPIO chip.

```bash
sudo adduser $USER gpio
```

**3. REBOOT YOUR PI:**
You must **reboot** for this change to take effect.
```bash
sudo reboot
```

## 2. Installation

Clone this repository and place the `gpiod_tm1638` package directory next to your project script.

```
my-project/
├── my_script.py
└── gpiod_tm1638/
    ├── __init__.py
    ├── TM1638s.py
    ├── TMBoards.py
    └── Font.py
```

## 3. Basic Usage

Here is a simple example to display "HELLO" on the first board.

```python
#!/usr/bin/env python3
import time
from gpiod_tm1638 import TMBoards

# --- Configuration ---
# BCM Pin numbers for your first board
DIO = 19
CLK = 13
STB = 26
# ---------------------

try:
    # Use a 'with' block to automatically handle GPIO cleanup
    # Note: On a Pi 5, the chip name is "gpiochip0"
    with TMBoards(DIO, CLK, STB, brightness=2, gpio_chip_name="gpiochip0") as tm:
        
        print("Test started. Displaying HELLO.")
        
        # Clear the display
        tm.clearDisplay()
        
        # Set segments 0-4 to "HELLO"
        tm.segments[0] = "HELLO"
        
        # Set the first two LEDs to Green and Red
        tm.leds[0] = True # Green LED 0
        tm.leds[1] = True # Green LED 1
        
        # Use sendData for Red LEDs (Bit 1)
        # Address 1 (LED 0), Value 2 (Red), Board 0
        tm.sendData(1, 2, 0) 

        print("Display is on. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print("\nExiting. Display will be cleared.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
```

## 4. API Notes

### Displays

`tm.segments[0] = "1234"` will display "1234" on the first four segments.

### LEDs

The `tm.leds[]` property is a simple helper for the Green/first color LED.
`tm.leds[0] = True`

To control bi-color LEDs, use `tm.sendData()`:
* **Address:** Use the odd addresses (1, 3, 5, 7, 9, 11, 13, 15).
* **Value:** `1` for Green (Bit 0), `2` for Red (Bit 1), `3` for Amber (Both).
* **Board Index:** `0` for the first board.

```python
# Turn on the Red LED for the 3rd segment (address 5) on the first board
tm.sendData(5, 2, 0)
```

### ⚠️ Important: Reading Keys

Due to a timing quirk in the TM1638 and the high speed of the `gpiod` library, you **must** use a specific sequence to read keys without causing bus conflicts.

The `tm.getData()` function is "dumb" and only reads bytes. You must manually send the "Read Key" command first.

**Correct Way to Read Keys:**

```python
# A 50ms delay is CRITICAL to prevent bus contention
time.sleep(0.05) 

# 1. Pull STB low for the specific board
tm._setStb(False, 0) # 0 = Board Index

# 2. Send the "Read Key" command (0x42)
tm._setDataMode(0x02, 0x00) # READ_MODE, INCR_ADDR

# 3. Call the "dumb" getData function
key_data = tm.getData(0) # 0 = Board Index

# 4. Pull STB high again
tm._setStb(True, 0)

# key_data is now [byte1, byte2, byte3, byte4]
if key_data != [0, 0, 0, 0]:
    print(f"Key data from board 0: {key_data}")
```
See `examples/test_keys.py` for a full implementation.

## License

The original `rpi-TM1638` library was licensed under the GNU v3 License. This derivative work retains that license.
