import blinka.blinkautil
import logging

#reboot_in_bootloader_mode

def print_port(args):
    port = blinka.blinkautil.find_serial_port()
    if port:
        logging.info(port)
    else:
        logging.error("Did not find a CircuitPython serial port")

def setup_argument_parser(parser):
    parser.description="Find the first CircuitPython serial port."
    parser.set_defaults(func=print_port)
