# The Blinka Command-Line Interface

This is intended to provide various useful commands for maintaining CircuitPython devices.

## Running

```
PS C:\Users\bcr00\Source\bcr\blinka-cli> python .\blinka.py --help
usage: blinka.py [-h] [-v | -q] [-l LOCALE] {backup} ...

Perform CircuitPython operations.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be chatty
  -q, --quiet           be quiet
  -l LOCALE, --locale LOCALE
                        specify the locale (default: en_US)

subcommands:
  {backup}              specify which operation to perform, use --help after the operation for operation-specific help
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

pip install pywin32
pip install semver
pip install pyserial