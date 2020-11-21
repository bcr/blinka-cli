import logging
import win32api

expected_user_mode_volume_names = [
    "CIRCUITPY",
]

expected_bootloader_mode_volume_names = [
    "PORTALBOOT",
]

# TODO: This is super Windows-centric right now. Other platforms should not
#       need `win32api` installed and will have their own way of finding the
#       root directory.

# https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python

def find_circuit_python_user_mode_root():
    drives = win32api.GetLogicalDriveStrings()
    logging.debug("raw drives is %s" % drives)
    drives = drives.split('\000')[:-1]
    logging.debug("final list of drives %s" % drives)

    # See if one has a volume name we like
    for drive in drives:
        volume_name = win32api.GetVolumeInformation(drive)[0]
        logging.debug("%s volume name is %s" % (drive, volume_name))
        if volume_name in expected_user_mode_volume_names:
            return drive

    logging.debug("did not find a suitable drive")
    return None