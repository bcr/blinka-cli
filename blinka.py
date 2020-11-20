import argparse
import locale
import logging
import tempfile

import commands.backup
import commands.bossa

commands = {
    "backup" : commands.backup,
    "bossa" : commands.bossa,
}

parser = argparse.ArgumentParser(description='Perform CircuitPython operations.')

chatty_group = parser.add_mutually_exclusive_group()
chatty_group.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="be chatty")
chatty_group.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="be quiet")

parser.add_argument("-l", "--locale", action="store", dest="locale", default = locale.getdefaultlocale()[0], help="specify the locale (default: %(default)s)")

# https://docs.python.org/3/library/argparse.html#sub-commands
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

# Set up locale
logging.info("Using %s for the locale" % options.locale)

with tempfile.TemporaryDirectory() as tempdir:
    logging.debug("Temporary directory is %s" % tempdir)
    options.tempdir = tempdir
    options.func(options)
