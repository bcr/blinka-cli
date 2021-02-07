import codecs
import blinka.fontutil
import logging
import string
import unicodedata

def output_glyph(glyph, unicode_codepoint, charset, file):
    x_offset = 0
    y_offset = -glyph.descent if glyph.descent else glyph.ascent - glyph.height

    try:
        char_name = unicodedata.name(unicode_codepoint).replace(' ', '_')
    except:
        char_name = "U+%06X" % ord(unicode_codepoint)

    logging.debug("Generating character '%s' %s" % (unicode_codepoint, char_name))

    encoded_char = unicode_codepoint.encode(charset)
    if len(encoded_char) > 0:
        # Bummer. Shouldn't happen for ASCII or 8859-x
        pass

    file.write("STARTCHAR %s\n" % char_name)
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
                file.write("%02X" % current_byte)
                current_byte = 0

        remainder = 8 - (x % 8)
        if remainder < 8:
            current_byte <<= remainder
            file.write("%02X" % current_byte)
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

def output_header(file, bounding_box):
    file.write("STARTFONT 2.1\n")
    file.write("COMMENT Created with blinka-cli <url:https://github.com/bcr/blinka-cli>\n")
    file.write("FONTBOUNDINGBOX %d %d %d %d\n" % (bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]))

    properties = {}
    properties['FONT_ASCENT'] = bounding_box[4]
    properties['FONT_DESCENT'] = bounding_box[5]
    if len(properties.keys()) > 0:
        # Output properties
        file.write("STARTPROPERTIES %d\n" % len(properties.keys()))
        for key in properties:
            file.write("%s %s\n" % (key, properties[key]))
        file.write("ENDPROPERTIES\n")

    file.write("CHARS\n")

def output_footer(file):
    file.write("ENDFONT\n")

def update_bounding(bounding_box, glyph):
    if not bounding_box:
        bounding_box = [0, 0, 0, 0, 0, 0]
    x = glyph.bitmap.width
    y = glyph.bitmap.height
    x_offset = 0
    y_offset = -glyph.descent if glyph.descent else glyph.ascent - glyph.height
    ascent = glyph.ascent
    descent = glyph.descent
    bounding_box[0] = max(bounding_box[0], x)
    bounding_box[1] = max(bounding_box[1], y)
    bounding_box[2] = min(bounding_box[2], x_offset)
    bounding_box[3] = min(bounding_box[3], y_offset)
    bounding_box[4] = max(bounding_box[4], ascent)
    bounding_box[5] = max(bounding_box[5], descent)
    return bounding_box

def get_chars_to_output(args):
    chars_to_output = None
    if args.chars_file:
        # load from file
        with codecs.open(args.chars_file, 'r', encoding='utf8') as f:
            chars_to_output = f.read()
            logging.debug(chars_to_output)
    elif args.chars:
        chars_to_output = args.chars
    else:
        chars_to_output = string.printable

    return chars_to_output

def do_font(args):
    logging.debug("Making a font from %s %d" % (args.fontpath, args.fontsize))
    font = blinka.fontutil.Font(args.fontpath, args.fontsize)
    filename = make_suggested_filename(font, args.fontsize)
    chars_to_output = get_chars_to_output(args)
    logging.info("Writing font to %s" % filename)
    with open(filename, "w") as file:
        char_array = list(chars_to_output)

        # https://github.com/adafruit/Adafruit_CircuitPython_Display_Text/blob/master/adafruit_display_text/label.py#L257
        # An "M" is required
        char_array.append('M')

        char_set = set(char_array)
        char_array = list(char_set)
        char_array.sort()

        # First we need the font bounding box. This means we have to go
        # through every single character we are going to output in order
        # to find the maximum bounding. You're welcome.
        bounding_box = None
        for char in char_array:
            glyph = font.glyph_for_character(char)
            bounding_box = update_bounding(bounding_box, glyph)

        output_header(file, bounding_box)
        for char in char_array:
            glyph = font.glyph_for_character(char)
            output_glyph(glyph, char, "ascii", file)
        output_footer(file)

def setup_argument_parser(parser):
    parser.description="Perform font management operations."
    parser.add_argument("--fontpath", action="store", dest="fontpath", help="specify the font", required=True)
    parser.add_argument("--fontsize", action="store", dest="fontsize", help="specify the font size", type=int, required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--printable", action="store_true", dest="printable", help="generate glyphs for all printable characters")
    group.add_argument("--chars", action="store", dest="chars", help="only generate glyphs for the specified characters")
    group.add_argument("--chars-file", action="store", dest="chars_file", help="only generate glyphs for the UTF-8 characters in file")

    parser.set_defaults(func=do_font)
