import blinkautil
import board
import fsutil
import logging
import os.path
import semver
import shutil
import time
import urlutil

warning_string = """
At this point I would like to:

1. Reboot your device in bootloader mode
2. Copy the firmware to the bootloader drive to update it

ALWAYS BACKUP YOUR CODE BEFORE INSTALLING OR UPDATING CIRCUITPYTHON

You can use the convenient "blinka backup" command to do this!

For more information please see https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython

OK, have you made your backup and are you ready to do this?"""

def confirm(prompt):
    entry = input("%s [y/N]" % prompt)
    print()
    return (entry == "y") or (entry == "Y")

def do_update(args):
    logging.debug("do_update")

    (version, board_id) = board.identify(args.root)
    board_id = args.board if args.board is not None else board_id

    logging.debug("board_id = %s" % board_id)
    logging.debug("Current CircuitPython version is %s" % version)

    if args.firmware_version is None:
        metadata = board.get_version_metadata(board_id)
        logging.debug("metadata %s" % metadata)
        target_firmware = next(version for version in metadata['versions'] if ('uf2' in version['extensions']) and (args.locale in version['languages']) and (args.stable == version['stable']))
        new_version = target_firmware['version']
        logging.debug("target_firmware %s" % target_firmware)
        logging.info("The latest available version is %s and you have version %s" % (new_version, version))
        logging.debug("comparing %s to %s", version, new_version)
        perform_update = (semver.compare(version, new_version) < 0)
        url = board.get_download_url(new_version, board_id, 'uf2', args.locale)
    else:
        # Forcing an update to a particular version

        new_version = args.firmware_version
        perform_update = True
        url = board.get_download_url(new_version, board_id, 'uf2', args.locale)

    if args.commit_hash is not None:
        s3_path = urlutil.find_firmware_by_hash(args.commit_hash, board_id, args.locale)
        if s3_path:
            perform_update = True
            url = urlutil.get_s3_url(s3_path)
        else:
            print("")

    if perform_update:
        # Do upgrade
        # Download UF2

        logging.debug("Final url is %s" % url)
        logging.info("Retrieving firmware from %s" % url)
        pathname = urlutil.get_local_file_from_url(url, args.tempdir)
        logging.debug("Firmware downloaded to %s" % pathname)
        if confirm(warning_string):
            # Reboot in bootloader mode
            logging.info("Rebooting device in bootloader mode")
            blinkautil.reboot_in_bootloader_mode(args.port)
            # Wait for things to settle down
            logging.info("Waiting a bit for things to settle")
            time.sleep(4)
            # Get root to copy to
            bootloader_root = fsutil.find_circuit_python_bootloader_mode_root()
            (_, filename) = os.path.split(pathname)
            # Copy it
            logging.info("Copying %s to %s" % (filename, bootloader_root))
            logging.debug("Performing shutil.copy('%s', '%s')" % (pathname, bootloader_root))
            shutil.copy(pathname, bootloader_root)
            # All done! Should be back in user mode if everything is OK
            logging.info("Waiting a bit for things to settle")
            time.sleep(9)
            (version, board_id) = board.identify(args.root)
            if version == new_version:
                logging.info("I checked the current version and it looks right! All updated.")
            else:
                logging.error("I tried to update, and I expected the current version to be %s and instead it is %s" % (new_version, version))
        pass
    else:
        logging.info("No upgrade required, thanks for checking!")

def setup_argument_parser(parser):
    parser.description="Updates your CircuitPython to the latest version."
    root = fsutil.find_circuit_python_user_mode_root()
    port = blinkautil.find_serial_port()
    parser.add_argument("-r", "--root", action="store", dest="root", default=root, help="specify the root directory of your CircuitPython (default: %(default)s)", required=root is None)
    parser.add_argument("-u", "--unstable", action="store_false", dest="stable", default = True, help="use the latest not-stable CircuitPython version instead of the stable version")
    parser.add_argument("--board", action="store", dest="board", help="specify the board type")
    parser.add_argument("--port", action="store", dest="port", default = port, help="the port for CircuitPython (default: %(default)s)", required=(port is None))
    parser.add_argument("--firmware-version", action="store", dest="firmware_version", help="the exact version you would like")
    parser.add_argument("--commit-hash", action="store", dest="commit_hash", help="the commit hash of the build you would like")
    parser.set_defaults(func=do_update)
