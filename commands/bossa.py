import blinkautil
import logging
import os
import re
import semver
import subprocess
import board
import urlutil

offsets = {
    "SAMD21" : "0x2000",
    "SAMD51" : "0x4000",
}

bossa_landing_page_url = "http://www.shumatech.com/web/products/bossa"
adafruit_bossa_url = "https://learn.adafruit.com/welcome-to-circuitpython/non-uf2-installation"

class BossaError(Exception):
    pass

def confirm(prompt):
    entry = input("%s [y/N]" % prompt)
    return (entry == "y") or (entry == "Y")

def process_output_bytes_to_string(bytes):
    # So this is a fairly typical problem, I have some pile of bytes that came
    # from the process execution. So what charset is that? Is it "the platform"
    # character set? Is it UTF-8? Does it depend on "which process?"
    #
    # The most conservative answer is probably to use iso-8859-1 which encodes
    # all 256 codepoints and won't fail (but might look like a dummy if given
    # UTF-8 sequences.)
    #
    # In the event that the data is not UTF-8 and has any characters outside
    # of the ASCII range, it is likely it will fail to parse because it won't
    # be valid UTF-8.
    #
    # Because I have faith in humanity, I am going to assume UTF-8 because I am
    # worldly and global.

    return bytes.decode('utf-8')

def get_bossa_version(args):
    final_version = None
    bossa_args = [args.bossa_path, "-h"]
    logging.debug("Executing %s" % ' '.join(bossa_args))
    result = subprocess.run(bossa_args, capture_output=True)
    logging.debug("returncode = %d", result.returncode)

    # Don't check returncode -- BOSSAC returns 1 when asking for help, and
    # we really don't care anyway, just as long as we can parse a version

    logging.debug("Stdout is %s" % result.stdout)

    # Parse out the first string that is "Version (something)<EOL>"
    final_version = re.findall(r"Version\s+(\S+)\s+", process_output_bytes_to_string(result.stdout))[0]
    logging.debug("final_version %s " % final_version)
    return final_version

def ensure_correct_bossa_version(args):
    version = get_bossa_version(args)
    version_requirement = ">=1.9.0"

    logging.debug("Comparing BOSSA version %s to %s" % (version, version_requirement))
    if semver.match(version, version_requirement) <= 0:
        complaint = "BOSSA version is %s and needs to match %s. Unable to continue. You can upgrade BOSSA at %s" % (version, version_requirement, bossa_landing_page_url)
        logging.fatal(complaint)
        raise BossaError(complaint)
    logging.debug("BOSSA version %s" % version)

def get_info(args):
    final_dict = None
    bossa_args = [args.bossa_path, "-p", args.port, "-i"]
    logging.debug("Executing %s" % ' '.join(bossa_args))
    result = subprocess.run(bossa_args, capture_output=True)
    logging.debug("returncode = %d", result.returncode)
    if result.returncode == 0:
        # Well good for us
        logging.debug("Stdout is %s" % result.stdout)
        lines = result.stdout.splitlines()
        final_dict = {}
        for line in lines:
            line = process_output_bytes_to_string(line)
            (key, value) = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            logging.debug("key = '%s' value = '%s'" % (key, value))
            final_dict[key] = value
    else:
        logging.debug("Stderr is %s" % result.stderr)
        stderr = process_output_bytes_to_string(result.stderr).splitlines()
        complaint = "BOSSA has a complaint: %s" % stderr[0]
        logging.fatal(complaint)
        raise BossaError(complaint)

    return final_dict

def execute_update(args, offset, pathname):
    bossa_args = [args.bossa_path, "-p", args.port, "-e", "-w", "-v", "-R", "--offset=%s" % offset, pathname]
    command_line = ' '.join(bossa_args)
    if confirm("I will be executing the command line:\n\n%s\n\nPLEASE REVIEW IT\nTo understand more about the risks go to %s\nReady to run this command?" % (command_line, adafruit_bossa_url)):
        logging.info("Executing %s" % command_line)
        result = subprocess.run(bossa_args)


def do_bossa(args):
    ensure_correct_bossa_version(args)
    info = get_info(args)
    device = info["Device"]
    address = None
    for start_address in offsets:
        if start_address in device:
            address = offsets[start_address]
            break
    logging.debug("Address for device %s is %s" % (device, address))

    # Find the latest firmware metadata
    metadata = board.get_version_metadata(args.board)
    logging.debug("board metadata %s" % metadata)

    target_firmware = next(version for version in metadata['versions'] if ('bin' in version['extensions']) and (args.locale in version['languages']) and (args.stable == version['stable']))
    logging.debug("target_firmware %s" % target_firmware)

    url = board.get_download_url(target_firmware, args.board, 'bin', args.locale)
    logging.debug("Final url is %s" % url)
    logging.info("Retrieving firmware from %s" % url)
    pathname = urlutil.get_local_file_from_url(url, args.tempdir)
    logging.debug("Firmware downloaded to %s" % pathname)

    execute_update(args, address, pathname)

# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def find_bossa_path():
    path = 'C:\\Program Files (x86)\\BOSSA\\bossac.exe'
    logging.debug("Checking for executableness of %s" % path)
    return path if is_exe(path) else None

def find_port():
    return blinkautil.find_serial_port()

def setup_argument_parser(parser):
    bossa_path = find_bossa_path()
    port = find_port()
    board = None
    parser.add_argument("--bossa-path", action="store", dest="bossa_path", default = bossa_path, help="specify the path to BOSSA (default: %(default)s)", required = (bossa_path is None))
    parser.add_argument("--port", action="store", dest="port", default = port, help="the port for the BOSSA bootloader (default: %(default)s)", required=(port is None))
    parser.add_argument("--board", action="store", dest="board", default = board, help="specify the board type (default: %(default)s)", required = (board is None))
    parser.add_argument("-u", "--unstable", action="store_false", dest="stable", default = True, help="use the latest not-stable CircuitPython version instead of the stable version")

    parser.set_defaults(func=do_bossa)
