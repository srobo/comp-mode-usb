"""code.py - Entrypoint for main CircuitPython routine."""
import json
import time

import board
import neopixel

# Orange is modified here to make it more distinct from yellow
corners = [0x00ff00, 0xff3300, 0xff00ff, 0xffff00]

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 4)
PIXELS.brightness = 0.02  # The LEDs are very bright


def set_corner(corner, arena=None):
    """Set LEDs 1/2 to the corner's colour, the LED set depends on the arena."""
    if arena == 'A':
        PIXELS[1] = corners[corner]
    elif arena == 'B':
        PIXELS[2] = corners[corner]
    else:
        PIXELS[1] = corners[corner]
        PIXELS[2] = corners[corner]


def heartbeat(led):
    """Fade up and back down, this takes 1 second."""
    for i in range(50, 255, 25):
        PIXELS[led] = (0, 0, i)
        time.sleep(0.05)

    for i in reversed(range(50, 255, 25)):
        PIXELS[led] = (0, 0, i)
        time.sleep(0.05)


def get_zone_from_file(filename):
    """
    Read the zone and arena from a metadata file.

    All LEDs are held blue if an error occurs.
    """
    try:
        with open(filename) as fp:
            config = fp.read()
            data = json.loads(config)

        return data['zone'], data['arena']
    except (OSError, ValueError, IndexError) as e:
        print(e)
        # All LEDs are set blue if the mode file is invalid
        PIXELS.fill(0x0000FF)
        while True:
            time.sleep(1)


# LEDs set to corner colour
zone, arena = get_zone_from_file('astoria.json')
set_corner(zone, arena)

while True:
    heartbeat(0)
