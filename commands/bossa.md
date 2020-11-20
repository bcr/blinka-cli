# The Bossa Command

<https://learn.adafruit.com/welcome-to-circuitpython/non-uf2-installation>

1. Versions of BOSSA before 1.9 are not compatible with CircuitPython
2. The offset for the write location needs to be set with the `--offset` parameter
    * `0x2000` for SAMD21 boards
    * `0x4000` for SAMD51 boards

To accommodate these constraints, the `bossa` subcommand does the following:

1. Upon start of the `bossa` subcommand, the `bossac` tool is run with the
   `-h` option to extract the version information output on the help screen.
2. If the version is not recent enough, processing stops, and you will not
   proceed to party.
3. The `bossac` tool is run with the `-i` option. This will produce output
   that indicates which device is attached.
4. Based on the device type, the offset is determined
    * If the device type contains the string "SAMD21" then the `0x2000` 
      offset is used
    * If the device type contains the string "SAMD51" then the `0x4000`     
      offset is used
    * Otherwise processing will stop
