import json
import logging
import os.path
import urlutil

# This is a mapping from the text in boot_log.txt to the board ID used in the firmware filenames

boards = {
    "Adafruit Feather M0 RFM69 with samd21g18": "feather_m0_rfm69",
    "Adafruit PyPortal Titano with samd51j20": "pyportal_titano",
}

download_url_template = "https://downloads.circuitpython.org/bin/{board}/{locale}/adafruit-circuitpython-{board}-{locale}-{version}.{extension}"

def get_boot_string(root):
    # Read first line of boot_out.txt
    filename = os.path.join(root, 'boot_out.txt')
    logging.debug("Reading line from %s" % filename)
    with open(filename, 'r') as f:
        return f.readline()

def identify(root):
    boot_string = get_boot_string(root)
    # Format is:
    # Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Feather M0 RFM69 with samd21g18
    parts = [item.strip() for item in boot_string.split(';')]
    boot_board = parts[1]
    logging.debug("boot_board = \"%s\"" % boot_board)

    return boards[boot_board]

def get_version_metadata(board_id):
    # This file has the metadata for all the boards. Go get it and find our board in it.
    url = 'https://raw.githubusercontent.com/adafruit/circuitpython-org/master/_data/files.json'
    logging.debug("Fetching metadata from %s" % url)
    all_metadata = urlutil.get_json_from_url(url)
    return next((x for x in all_metadata if x['id'] == board_id), None)

def get_download_url(version, board, extension, locale):
    return download_url_template.format(version = version['version'], locale = locale, extension = extension, board = board)