# Notes about Font support

Some BDF info is here <https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format>

Also here <https://www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5005.BDF_Spec.pdf>

The compatibility required is basically the BDF implementation found in
<https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/blob/master/adafruit_bitmap_font/bdf.py>

Based on that implementation, I see the following lines as relevant:


| Parameter | Usage |
| --- | --- |
| `STARTFONT` | Line must start with `STARTFONT 2.1` |
| `BBX` | Parsed into `x`, `y`, `x_offset` and `y_offset` and used as-is as integers. The bitmap is `x` by `y`|
| `BITMAP` | Each line after here has one row of the bitmap packed in bytes |
| `ENCODING` | This one is key, it has the code point for your char |
| `DWIDTH` | Parsed into `shift_x` and `shift_y` |
| `FONTBOUNDINGBOX` | Used |
| `SIZE` | Data is stored in `point_size`, `x_resolution` and `y_resolution` but does not appear to be used |
| `CHARS` | Used as a sentinel to know when metadata ends |
| `STARTCHAR` | Used as a sentinel to know when a char starts |
| `ENDCHAR` | Used as a sentinel to know when a char ends |
| `COMMENT` | Everything ignored as appropriate, no current metadata hacks |

There are also "properties" (found in the `STARTPROPERTIES` section) that are required.

| Property | Usage |
| --- | --- |
| `FONT_ASCENT` | Parsed into `_ascent` |
| `FONT_DESCENT` | Parsed into `_descent` |

<https://adafruit.github.io/web-bdftopcf/> is potentially interesting.
