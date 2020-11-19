import argparse
import board
import locale
import logging
import commands.backup

commands = {
    "backup" : commands.backup,
}

parser = argparse.ArgumentParser(description='Perform CircuitPython operations.')

chatty_group = parser.add_mutually_exclusive_group()
chatty_group.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="be chatty")
chatty_group.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="be quiet")

parser.add_argument("-r", "--root", action="store", dest="root", help="specify the root directory of your CircuitPython")
parser.add_argument("-l", "--locale", action="store", dest="locale", default = locale.getdefaultlocale()[0], help="specify the locale (default: %(default)s)")
parser.add_argument("-b", "--board", action="store", dest="board_id", help="specify the board type")

# https://docs.python.org/3/library/argparse.html#sub-commands
#parser.add_argument("operation", choices = commands.keys(), help="specify which operation to perform, use --help after the operation for help about the operation")

subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True, help="specify which operation to perform, use --help after the operation for operation-specific help")
for command in commands:
    new_parser = subparsers.add_parser(name=command)
    commands[command].setup_argument_parser(new_parser)

options = parser.parse_args()

# Set up logging
if not options.quiet:
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG if options.verbose else logging.INFO)

logging.debug("options = %s" % options)

# Set up root directory
options.root = options.root if options.root is not None else "E:\\"
logging.info("Using %s for the root directory" % options.root)

# Set up locale
logging.info("Using %s for the locale" % options.locale)

# Determine board ID
options.board_id = board.identify(options.root) if not options.board_id else options.board_id
logging.info("Using %s for the board ID" % options.board_id)

# logging.info("\N{grinning face} Found board %s" % board_id)

#print(board.get_version_metadata(board_id)['versions'][0])


options.func(options)
