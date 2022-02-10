import time

import board
import neopixel

# Orange is modified here to make it more distinct from yellow
# Remember to update the colours in src/code.py if you change them here
corners = [0x00ff00, 0xff3300, 0xff00ff, 0xffff00]

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 4)
PIXELS.brightness = 0.02  # The LEDs are very bright

# Preview corner colours
PIXELS[:] = corners
while True:
    time.sleep(1)
