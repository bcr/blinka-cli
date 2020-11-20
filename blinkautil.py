import logging
import serial
import time

reboot_to_bootloader_script = """
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
microcontroller.reset()
"""

def string_to_script_bytes(script):
    return ("\r\n".join(script.split("\n"))).encode('ASCII')

def reboot_in_bootloader_mode(port):
    # Connect to the port
    logging.debug("connecting to port %s" % port)
    connection = serial.Serial(port)

    # Not sure there's a lot of science here -- the idea is to honk on the
    # board until we can start typing in the REPL, and then send our fancy
    # reboot script

    logging.debug("Sending breaks to wake up")
    for _ in range(3):
        connection.write(b"\x03")
        time.sleep(0.2)

    # Run the reboot script
    logging.debug("Sending script")
    connection.write(string_to_script_bytes(reboot_to_bootloader_script))

    # If we do this right our connection should be gone
