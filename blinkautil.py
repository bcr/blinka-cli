import logging
import serial
import serial.tools.list_ports
import time

reboot_to_bootloader_script = """
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
microcontroller.reset()
"""

# Some VID / PIDs I saw

# Name                          VID     PID
# PyPortal Titano (bootloader)  0x239A  0x0035
# PyPortal Titano (user)        0x239A  0x8054
# Feather M0 RFM69 (bootloader) 0x239A  0x000B
# Feather M0 RFM69 (user)       0x239A  0x80D2

# These are the known USB VIDs for compatible boards
vids = [
    0x239A, # Adafruit
]

def string_to_script_bytes(script):
    return ("\r\n".join(script.split("\n"))).encode('ASCII')

def reboot_in_bootloader_mode(port):
    # Connect to the port

    try:
        logging.debug("connecting to port %s" % port)
        connection = serial.Serial(port)
    except serial.serialutil.SerialException as e:
        if "FileNotFoundError" in e.args[0]:
            logging.critical("Could not open port %s -- are you sure you have the right name?" % port)
        elif "PermissionError" in e.args[0]:
            logging.critical("Could not open port %s -- is it open in a terminal program?" % port)
        raise

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

def find_serial_port():
    for port in serial.tools.list_ports.comports():
        logging.debug("found port %s vid %04x" % (port, port.vid))
        if port.vid in vids:
            logging.debug("found matching vid = %04x pid = %04x" % (port.vid, port.pid))
            return port.device
