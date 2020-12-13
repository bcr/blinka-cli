import fontutil
import logging
import unicodedata

def output_glyph(glyph, unicode_codepoint, charset, file):
    logging.debug("Generating character '%s'" % unicode_codepoint)
    x_offset = glyph.advance_width - glyph.bitmap.width
    y_offset = -glyph.descent if glyph.descent else glyph.ascent - glyph.height
    encoded_char = unicode_codepoint.encode(charset)
    if len(encoded_char) > 0:
        # Bummer. Shouldn't happen for ASCII or 8859-x
        pass
    file.write("STARTCHAR %s\n" % unicodedata.name(unicode_codepoint).replace(' ', '_'))
    file.write("ENCODING %d\n" % encoded_char[0])
    file.write("DWIDTH %d %d\n" % (glyph.advance_width, 0))
    file.write("BBX %d %d %d %d\n" % (glyph.bitmap.width, glyph.bitmap.height, x_offset, y_offset))
    file.write("BITMAP\n")
    for y in range(glyph.height):
        x = 0
        current_byte = 0
        while x < glyph.bitmap.width:
            current_byte <<= 1
            current_byte |= 1 if glyph.bitmap.pixels[y * glyph.bitmap.width + x] else 0
            x += 1
            if (x % 8) == 0:
                file.write("%02X " % current_byte)
                current_byte = 0

        remainder = 8 - (x % 8)
        if remainder < 8:
            current_byte <<= remainder
            file.write("%02X " % current_byte)
        file.write("\n")
    file.write("ENDCHAR\n")

def make_suggested_filename(font, size):
    family_name = font.face.family_name.decode("utf-8")
    style_name = font.face.style_name.decode("utf-8")
    final_name = "%s %s %d" % (family_name, style_name, size)
    final_name = final_name.replace(' ', '-')
    final_name += ".bdf"
    logging.debug("Final filename is %s" % final_name)
    return final_name

def output_header(file):
    file.write("STARTFONT 2.1\n")
    file.write("CHARS\n")

def output_footer(file):
    file.write("ENDFONT\n")

def do_font(args):
    logging.debug("Making a font from %s %d" % (args.fontpath, args.fontsize))
    font = fontutil.Font(args.fontpath, args.fontsize)
    filename = make_suggested_filename(font, args.fontsize)
    chars_to_output = "Hello, world!"
    logging.info("Writing font to %s" % filename)
    with open(filename, "w") as file:
        output_header(file)
        char_array = list(chars_to_output)
        char_set = set(char_array)
        char_array = list(char_set)
        char_array.sort()
        for char in char_array:
            glyph = font.glyph_for_character(char)
            output_glyph(glyph, char, "ascii", file)
        output_footer(file)

def setup_argument_parser(parser):
    parser.description="Perform font management operations."
    parser.add_argument("--fontpath", action="store", dest="fontpath", help="specify the font", required=True)
    parser.add_argument("--fontsize", action="store", dest="fontsize", help="specify the font size", type=int, required=True)
    parser.set_defaults(func=do_font)
