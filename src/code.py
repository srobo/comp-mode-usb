import time
import board
import neopixel

# Orange is modified here to make it more distinct from yellow
corners = [0x00ff00, 0xff3300, 0xff00ff, 0xffff00]

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 4)
PIXELS.brightness = 0.02  # The LEDs are very bright

ZONE = 1


def set_corner(corner, arena=None):
    "Set LEDs 1/2 to the corner's colour, the LED set depends on the arena"
    if arena == 'A':
        PIXELS[1] = corners[corner]
    elif arena == 'B':
        PIXELS[2] = corners[corner]
    else:
        PIXELS[1] = corners[corner]
        PIXELS[2] = corners[corner]


def heartbeat(led):
    "Fade up and back down, this takes 1 second"
    for i in range(50, 255, 25):
        PIXELS[led] = (0, 0, i)
        time.sleep(0.05)

    for i in reversed(range(50, 255, 25)):
        PIXELS[led] = (0, 0, i)
        time.sleep(0.05)


# LEDs set to corner colour
set_corner(ZONE)

while True:
    heartbeat(0)
