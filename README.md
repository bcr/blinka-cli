# The Blinka Command-Line Interface

This is intended to provide various useful commands for maintaining CircuitPython devices.

## Running

```
PS C:\Users\bcr00\Source\bcr\blinka-cli> python .\blinka.py --help    
usage: blinka.py [-h] [-v] [-l LOCALE] {backup,bossa,bootloader,update} ...

Perform CircuitPython operations.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be chatty
  -l LOCALE, --locale LOCALE
                        specify the locale (default: en_US)

subcommands:
  {backup,bossa,bootloader,update}
                        specify which operation to perform, use --help after the operation for operation-specific help
```

## Commands

### Backup

### Update (coming soon)

## Tasks

* Back up CircuitPython contents
* Maintain CircuitPython
    * Compare version and upgrade if newer version available
    * Allow for installing pre-release version
    * Force reinstall of current version
    * Force install a particular version
* Maintain libraries
    * Force reinstall of installed libraries to corresponding CircuitPython version

## Installation Details

pip install pywin32 (only on Windows systems)
pip install semver
pip install pyserial
pip install dirsync

## Observations About Namespaces

Within CircuitPython there are a lot of different places where there are
name / numberspaces:

* Processors
  * M0, M4
  * SAMD21, SAMD51
* Platform identifiers (from user mode)
  * Adafruit Feather M0 RFM69 with samd21g18
  * Adafruit PyPortal with samd51j20
* Board IDs (firmware root names)
  * feather_m0_rfm69
  * pyportal_titano
* USB VID / PID
  * Adafruit VID
  * PIDs differ between bootloader and user mode COM ports
* Mounted disk volume labels
  * CIRCUITPY for user mode
  * LOTS for bootloader mode
    * `BOOT` is used a lot for a suffix
    * `shIRtty` mixed case, no `BOOT`
    * `ARCADE-D5` dash, no `BOOT`
    * `Grove Zero` mixed case, space in name, no `BOOT`
* `os.uname()` information
  * `(sysname='samd51', nodename='samd51', release='6.0.0', version='6.0.0 on 2020-11-16', machine='Adafruit PyPortal Titano with samd51j20')`


Some problems I have encountered:

* In bootloader mode there is not enough information to find the Board ID
  (in this case, is it a Titano? I know first-hand that the Titano firmware
  is materially different than the non-Titano PyPortal)
```
PS C:\Users\bcr00\Source\bcr\blinka-cli> type E:\INFO_UF2.TXT
UF2 Bootloader v1.23.1-adafruit.1-89-gcfdd5ba SFHWRO
Model: PyPortal M4 Express
Board-ID: SAMD51J20A-PyPortal-v0
```
* Mapping from the Platform Identifer to the Board ID seems fragile
  * Other manufacturers may not be as careful with naming
    * `J&J Studios datum-Distance with None` -- the None processor
    * `SparkFun Qwiic Micro with samd21e18` -- there is both
      `sparkfun_qwiic_micro_no_flash` and `sparkfun_qwiic_micro_with_flash`
      with this Platform Identifier
    * `ndGarage[n°] Bit6: FeatherSnow-v2 with samd21e18` -- a UTF-8 party
