import fontutil
import logging

def output_glyph(glyph):
    print("height = %d, ascent = %d, descent = %d" % (glyph.height, glyph.ascent, glyph.descent))
    x_offset = glyph.advance_width - glyph.bitmap.width
    y_offset = -glyph.descent if glyph.descent else glyph.ascent - glyph.height
    print("BBX %d %d %d %d" % (glyph.bitmap.width, glyph.bitmap.height, x_offset, y_offset))
    for y in range(glyph.height):
        x = 0
        current_byte = 0
        while x < glyph.bitmap.width:
            current_byte <<= 1
            current_byte |= 1 if glyph.bitmap.pixels[y * glyph.bitmap.width + x] else 0
            x += 1
            if (x % 8) == 0:
                print("%02X " % current_byte, end='')
                current_byte = 0

        remainder = 8 - (x % 8)
        if remainder < 8:
            current_byte <<= remainder
            print("%02X " % current_byte, end='')
        print()

def make_suggested_filename(font, size):
    family_name = font.face.family_name.decode("utf-8")
    style_name = font.face.style_name.decode("utf-8")
    final_name = "%s %s %d" % (family_name, style_name, size)
    final_name = final_name.replace(' ', '-')
    final_name += ".bdf"
    logging.debug("Final filename is %s" % final_name)

def do_font(args):
    logging.debug("Making a font from %s %d" % (args.fontpath, args.fontsize))
    font = fontutil.Font(args.fontpath, args.fontsize)
    make_suggested_filename(font, args.fontsize)
    letter = 'e'
    logging.debug("Here is a letter %s" % letter)
    glyph = font.glyph_for_character(letter)
    print(repr(glyph.bitmap))
    output_glyph(glyph)

def setup_argument_parser(parser):
    parser.description="Perform font management operations."
    parser.add_argument("--fontpath", action="store", dest="fontpath", help="specify the font", required=True)
    parser.add_argument("--fontsize", action="store", dest="fontsize", help="specify the font size", type=int, required=True)
    parser.set_defaults(func=do_font)
