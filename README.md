# Competition Mode USB
An implementation of the [Metadata USBs](https://srobo.github.io/astoria/usage.html#metadata-usbs) in CircuitPython using an Adafruit Neo Trinkey.

# Configuring a Neo Trinkey

The Neo Trinkey does not come with the CircuitPython bootloader installed.

To install the bootloader, plug the Trinkey and double press the reset button.
All 4 LEDs should now be green and a TRINKEYBOOT drive should be visible, if they are red there is a problem with the USB connection.
Download the CircuitPython bootloader from the [circuitpython website](https://circuitpython.org/board/neopixel_trinkey_m0/) and drag the uf2 file onto the TRINKEYBOOT drive.
The Neo Trinkey will then reboot and a CIRCUITPY drive will appear.

Now the bootloader is installed copy the contents of the `src/` folder into CiRCUITPY.
Once the Trinkey reboots there will be a SR_COMP_USB drive.
This is pre-configured to zone 2 of arena A, to change this see [Setting the Zone](#setting-the-zone).

# Setting the Zone

In the default mode the SR_COMP_USB drive is read-only, to be able to write to the drive boot into [safe-mode](https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting#safe-mode-3105351-27) by pressing the reset button while the the LEDs are flashing yellow, this occurs around 700ms after boot.

The astoria.json can then be replaced with one that has the zone updated.

## __DO NOT EDIT FILES ON SR_COMP_USB__
You will notice that SR_COMP_USB is only around 50kB so if editors try to generate cache files they quickly fill the disk.
Additionally the microcontroller resets when files are edited to load in their changes which can cause editors to corrupt the files.
Instead, edit the files on your computer and copy the updated files across.

If you did not heed this warning and have broken the drive follow [these instructions](https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting#circuitpy-drive-issues-2978456-26) to erase the filesystem and start again.

# Understanding the Reset Modes

Pressing the reset button while using the Trinkey can enter different modes.
The important thing to remember is that if all LEDs are the same colour, either constant or flashing, you are not in the operating mode.
Pressing reset once should restart the Trinkey back into operating mode.

If you hold down the reset button the Trinkey will not start until the button is released.
Pressing the reset button within 500ms of boot will enter into bootloader and all the LEDs will be a constant red or green.
If you press the reset button between 500ms and 1000ms of booting you will enter safe mode and all the LEDs will flash yellow three times every few seconds.
All these modes can be exited by pressing the reset button once.

If the LEDs are all blue the `astoria.json` file is invalid.
Any other uncaught exception will cause the LEDs to flash red.
In both these cases you should check the  `astoria.json` file, remembering __to not edit files directly on the Trinkey__.

![CircuitPython Boot Sequence](https://cdn-learn.adafruit.com/assets/assets/000/106/229/original/circuitpython_CircuitPython_Boot_Sequence_7.jpg)

# Other Notes
## json.py
Devices running CircuitPython with less than 2MB of flash do not have the built-in JSON library included.
The only way to include Adafruit's JSON library would be to compile a custom CircuitPython bootloader.
Since we are not concerned about the speed of JSON parsing we include our own limited JSON library, written in Python.

## Viewing Corner Colours
An alternative program is provided in the `demo/` directory to view all 4 corner colours at once.
Load this the same way as the regular code above.

## Debugging errors
Since we've disabled the serial terminal you cannot normally view what error is causing the Trinkey to crash.
A workaround for this is to boot into safe mode, which will re-enable the serial terminal.

Once you connect to the serial terminal, press a key to enter the REPL and enter `import code`.
This will run the standard code and allow you to view the error.

Note, generally the import command will not return so use Ctrl-C to be ale to enter more commands.

