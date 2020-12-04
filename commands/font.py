import fontutil
import logging

def do_font(args):
    logging.debug("Making a font from %s %d" % (args.fontpath, args.fontsize))
    font = fontutil.Font(args.fontpath, args.fontsize)
    logging.debug("Here is a letter e")
    character = font.render_character("e")
    print(repr(character))

def setup_argument_parser(parser):
    parser.description="Perform font management operations."
    parser.add_argument("--fontpath", action="store", dest="fontpath", help="specify the font", required=True)
    parser.add_argument("--fontsize", action="store", dest="fontsize", help="specify the font size", type=int, required=True)
    parser.set_defaults(func=do_font)
