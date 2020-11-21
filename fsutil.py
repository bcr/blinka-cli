import logging
import win32api

expected_user_mode_volume_names = [
    "CIRCUITPY",
]

expected_bootloader_mode_volume_names = [
    "PORTALBOOT", 'ND7BOOT', 'FTHRCANBOOT', 'SAMD21', 'E54XBOOT', 'PEWBOOT',
    'MKRZEROBOOT', 'GEMINIBOOT', 'PYCUBEDBOOT', 'METROM4BOOT', 'MKR1300',
    'shIRtty', 'ROBOM4BOOT', 'NANOBOOT', 'RCBOOT', 'HALLOM4BOOT', 'MINISAMBOOT',
    'ITSYBOOT', 'TRELM4BOOT', 'HONKBOOT', 'BADGEBOOT', 'ARCADE-D5', 'Grove Zero',
    'CMDBOOT', 'FEATHERBOOT', 'SPARKFUN', 'ROBOTICS', 'METROBOOT', 'GEMMABOOT',
    'BOOKBOOT', 'SNEKBOOT', 'SERPENTBOOT', 'ROBOM0BOOT', 'USBHUBBOOT', 'RADIOBOOT',
    'PIRKEYBOOT', 'CRICKITBOOT', 'SAME54', 'MKR1000', 'TRINKETBOOT', 'FLUFFBOOT',
    'SENSEBOX', 'ND6BOOT', 'BADGELCBOOT', 'GCM4BOOT', 'CC03', 'QTPY_BOOT',
    'UARTLOGBOOT', 'AUTOMAT', 'BOOT', 'SOLBOOT', 'CPLAYBOOT', 'CS11',
    'SAM32BOOT', 'HALLOWBOOT', 'ITSYM4BOOT', 'PYGAMERBOOT', 'ZEROBOOT', 'MASKM4BOOT',
    'UCHIPYBOOT', 'PYBADGEBOOT'
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

def find_circuit_python_bootloader_mode_root():
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

    logging.debug("did not find a suitable drive")
    return None