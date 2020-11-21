import blinkautil
import logging

#reboot_in_bootloader_mode

def reboot_in_bootloader_mode(args):
    logging.info("Rebooting device in bootloader mode")
    blinkautil.reboot_in_bootloader_mode(args.port)

def setup_argument_parser(parser):
    parser.description="Reboot your device in bootloader mode."
    port = blinkautil.find_serial_port()
    parser.add_argument("--port", action="store", dest="port", default = port, help="the port for the BOSSA bootloader (default: %(default)s)", required=(port is None))
    parser.set_defaults(func=reboot_in_bootloader_mode)
