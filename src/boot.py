"""
boot.py

This file is executed before the USB connection is setup so we can alter what
USB devices are created.
"""
import storage
import usb_cdc

# Make USB mount read-only (to host), this can only be done in boot.py
storage.remount('/', readonly=False)  # readonly here applies to MCU not host

# Set the name the mass storage appears as,
# this can only be done while the storage is writable to the microcontroller
m = storage.getmount("/")
if m.label != 'SR_COMP_USB':
    m.label = "SR_COMP_USB"

# Disable serial console
usb_cdc.disable()
