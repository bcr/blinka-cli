import argparse
import locale
import logging
import tempfile

import blinka.commands.backup
import blinka.commands.bossa
import blinka.commands.bootloader
import blinka.commands.update
import blinka.commands.sync
import blinka.commands.port
import blinka.commands.font
import blinka.commands.updatelibs

# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

def main():
    commands = {
        "backup" : blinka.commands.backup,
        "bossa" : blinka.commands.bossa,
        "bootloader" : blinka.commands.bootloader,
        "update" : blinka.commands.update,
        "sync" : blinka.commands.sync,
        "port" : blinka.commands.port,
        "font" : blinka.commands.font,
        "updatelibs" : blinka.commands.updatelibs,
    }

    # Do some initial logging setup -- this really needs to be here, before you do
    # stuff with argparse. Trust me on this.
    logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)

    # Put in some emojis for fun
    emojis = {
        logging.DEBUG       : "\N{Nerd Face}",
        logging.INFO        : "\N{Thumbs Up Sign}",
        logging.WARNING     : "\N{Worried Face}",
        logging.ERROR       : "\N{Pouting Face}",
        logging.CRITICAL    : "\N{Serious Face With Symbols Covering Mouth}",
    }

    for emoji in emojis:
        logging.addLevelName(emoji, emojis[emoji])

    parser = argparse.ArgumentParser(description='Perform CircuitPython operations.')

    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="be chatty")
    parser.add_argument("-l", "--locale", action="store", dest="locale", default = locale.getdefaultlocale()[0], help="specify the locale (default: %(default)s)")

    # https://docs.python.org/3/library/argparse.html#sub-commands
    subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True, help="specify which operation to perform, use --help after the operation for operation-specific help")
    for command in commands:
        new_parser = subparsers.add_parser(name=command)
        commands[command].setup_argument_parser(new_parser)

    options = parser.parse_args()

    # Change logging level if required
    logging.getLogger().setLevel(logging.DEBUG if options.verbose else logging.INFO)

    with tempfile.TemporaryDirectory() as tempdir:
        options.tempdir = tempdir
        logging.debug("options = %s" % options)
        options.func(options)
