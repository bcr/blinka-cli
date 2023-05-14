import json
import logging
import os.path
import pkgutil
import re
import blinka.urlutil

# This is a mapping from the text in boot_log.txt to the board ID used in the firmware filenames
boards = json.loads(pkgutil.get_data(__name__, "board_id_map.json"))

download_url_template = "https://downloads.circuitpython.org/bin/{board}/{locale}/adafruit-circuitpython-{board}-{locale}-{version}.{extension}"

def get_boot_info(root):
    # Read first line of boot_out.txt
    filename = os.path.join(root, 'boot_out.txt')
    logging.debug("Reading boot info from %s" % filename)
    return_dict = {}
    with open(filename, 'r') as f:
        id = f.readline().rstrip()
        return_dict['__id'] = id
        return_dict['__version'] = re.search(r"\s+(\d\S+)", id).group(1)
        for line in f:
            split = line.rstrip().split(':')
            if len(split) > 1:
                return_dict[split[0]] = split[1]

    return return_dict            

def identify(root):
    boot_info = get_boot_info(root)
    logging.debug("boot_info is %s" % boot_info)

    version = boot_info['__version']

    board_id = None
    if "Board ID" in boot_info:
        board_id = boot_info["Board ID"]
    else:
        boot_string = boot_info['__id']
        # Format is:
        # Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Feather M0 RFM69 with samd21g18
        parts = [item.strip() for item in boot_string.split(';')]
        boot_board = parts[1]
        logging.debug("boot_board = \"%s\"" % boot_board)
        board_id = boards.get(boot_board)

    return (version, board_id)

def get_version_metadata(board_id):
    # This file has the metadata for all the boards. Go get it and find our board in it.
    url = 'https://raw.githubusercontent.com/adafruit/circuitpython-org/master/_data/files.json'
    logging.debug("Fetching metadata from %s" % url)
    all_metadata = blinka.urlutil.get_json_from_url(url)
    return next((x for x in all_metadata if x['id'] == board_id), None)

def get_download_url(version, board, extension, locale):
    return download_url_template.format(version = version, locale = locale, extension = extension, board = board)