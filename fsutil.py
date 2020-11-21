import logging
import platform
if platform.system() == "Windows":
    import win32api
    use_windows_api = True
elif platform.system() == "Linux":
    # Running on linux
    import os
    import getpass
    use_windows_api = False

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

def find_circuit_python_user_mode_root(win=use_windows_api):
    if win:
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
    else:
        for drive in os.listdir("/media/{}".format(getpass.getuser())):
            logging.debug("volume name is %s" % drive)
            if drive in expected_user_mode_volume_names:
                return "/media/{}/{}".format(getpass.getuser(), drive)

    logging.debug("did not find a suitable drive")
    return None

def find_circuit_python_bootloader_mode_root(win=use_windows_api):
    if win:
        drives = win32api.GetLogicalDriveStrings()
        logging.debug("raw drives is %s" % drives)
        drives = drives.split('\000')[:-1]
        logging.debug("final list of drives %s" % drives)

        # See if one has a volume name we like
        for drive in drives:
            volume_name = win32api.GetVolumeInformation(drive)[0]
            logging.debug("%s volume name is %s" % (drive, volume_name))
            if volume_name in expected_bootloader_mode_volume_names:
                return drive
    else:
        for drive in os.listdir("/media/{}".format(getpass.getuser())):
            logging.debug("volume name is %s" % drive)
            if drive in expected_bootloader_mode_volume_names:
                return "/media/{}/{}".format(getpass.getuser(), drive)

    logging.debug("did not find a suitable drive")
    return None