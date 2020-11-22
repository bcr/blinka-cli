from datetime import datetime
import fsutil
import logging
import os
import shutil

# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
def backup(args):
    logging.info("Archiving %s to %s" % (args.root, args.filename))
    shutil.make_archive(args.filename, 'zip', args.root)

def find_root():
    return fsutil.find_circuit_python_user_mode_root()

def setup_argument_parser(parser):
    parser.description="Saves a copy of the filesystem on a CircuitPython device."
    default_filename = datetime.now().strftime('backup-%Y-%m-%d-%H-%M-%S%z.zip')
    root = find_root()
    parser.add_argument("-f", "--filename", action="store", dest="filename", default = default_filename, help="specify the filename to put the backup (default: %(default)s)")
    parser.add_argument("-r", "--root", action="store", dest="root", default=root, help="specify the root directory of your CircuitPython (default: %(default)s)", required=root is None)
    parser.set_defaults(func=backup)
