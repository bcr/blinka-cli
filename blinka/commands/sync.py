import dirsync
import blinka.fsutil
import logging

def sync(args):
    logging.info("Synchronizing %s to %s" % (args.root, args.local))
    dirsync.sync(args.root, args.local, 'sync', logger=logging)

def find_root():
    return blinka.fsutil.find_circuit_python_user_mode_root()

def setup_argument_parser(parser):
    parser.description="Keeps a local directory in sync with CircuitPython. UNDER DEVELOPMENT."
    root = find_root()
    local = '.'
    parser.add_argument("-r", "--root", action="store", dest="root", default=root, help="specify the root directory of your CircuitPython (default: %(default)s)", required=root is None)
    parser.add_argument("-l", "--local", action="store", dest="local", default=local, help="specify the root directory of your local copy (default: %(default)s)")
    parser.set_defaults(func=sync)
