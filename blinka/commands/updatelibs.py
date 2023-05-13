from datetime import datetime
import blinka.fsutil
import logging
import os
import semver
import shutil
from urllib.parse import urlparse
import zipfile

class ReleaseManager:
    def __init__(self):
        self.update_metadata()
        self.update_library_list()

    def update_metadata(self):
        url = "https://api.github.com/repos/adafruit/Adafruit_CircuitPython_Bundle/releases/latest"
        logging.debug("getting metadata from %s" % url)
        self.metadata = blinka.urlutil.get_json_from_url(url)

    def update_library_list(self):
        # The .json file that is in the assets metadata is the library list
        for asset in self.metadata['assets']:
            url = asset['browser_download_url']
            (_, filename) = os.path.split(urlparse(url).path)
            (_, extension) = os.path.splitext(filename)
            if extension == '.json':
                logging.debug("getting library list from %s" % url)
                self.library_list = blinka.urlutil.get_json_from_url(url)
                self.library_set = set(self.library_list.keys())
                break

    def get_dependencies(self, libraries):
        dependencies = set()
        for library in libraries:
            dependencies.update(self.library_list[library]['dependencies'])
        logging.debug("dependencies are %s" % dependencies)
        return dependencies

    def get_libraries(self, version, tempdir):
        target_pattern = "adafruit-circuitpython-bundle-%s.x-mpy" % version.major
        logging.debug("looking for asset %s" % target_pattern)
        final_url = None
        for asset in self.metadata['assets']:
            if asset['name'].startswith(target_pattern):
                final_url = asset['browser_download_url']
                break
        logging.info("Retrieving libraries from %s" % final_url)
        self.libraries_pathname = blinka.urlutil.get_local_file_from_url(final_url, tempdir)
        # self.libraries_pathname = "/Users/blake/Downloads/adafruit-circuitpython-bundle-8.x-mpy-20230512.zip"

    def sanity_check(self, path):
        # This might do something in the future. There's enough removing files
        # and directories that it just seems like something could go wrong and
        # you end up somewhere you don't want. Like /lib/ on Linux for instance.
        pass

    def update_or_install_libraries(self, libraries, root):
        cleaned = set()

        with zipfile.ZipFile(self.libraries_pathname) as library_file:
            for file in library_file.infolist():
                # The next thing after /lib/ is the library name
                # either a directory or an mpy file
                index = file.filename.find('/lib/')
                if index == -1:
                    continue

                filename = file.filename[index + 5:] # +5 is the length of /lib/

                # So now we have:
                # library.mpy
                # library/something

                is_directory = False
                index = filename.find('/')
                if index == -1:
                    (library, _) = os.path.splitext(filename)
                else:
                    library = filename[:index]
                    is_directory = True

                # logging.debug("library %s" % library)

                # See if it's in our libraries
                if not library in libraries:
                    continue

                # Clean out any existing stuff if needed
                if not library in cleaned:
                    destination = os.path.join(root, 'lib', library)
                    self.sanity_check(destination)
                    logging.debug("Cleaning out %s" % destination)
                    if os.path.isdir(destination):
                        shutil.rmtree(destination)
                    else:
                        destination += '.mpy'
                        if os.path.isfile(destination):
                            os.remove(destination)

                    cleaned.add(library)

                    logging.info("Updating %s" % library)

                # Extract it, making any required parent directories
                destination = os.path.join(root, 'lib', filename)

                # Make any required directories
                if is_directory:
                    (prefix, _) = os.path.split(destination)
                    logging.debug("making directory %s" % prefix)
                    self.sanity_check(prefix)
                    os.makedirs(prefix, exist_ok=True)

                # Extract it
                logging.debug("extracting %s to %s" % (file, destination))
                self.sanity_check(destination)
                with library_file.open(file.filename) as contents, open(destination, 'wb') as output_file:
                    shutil.copyfileobj(contents, output_file)

def find_current_libraries(root):
    found_libraries = set()
    lib_directory = os.path.join(root, 'lib')
    logging.debug("finding existing installed libraries in %s" % lib_directory)
    for entry in os.listdir(lib_directory):
        if entry.endswith('.mpy'):
            entry = entry[0:entry.find('.mpy')]

        found_libraries.add(entry)
    logging.debug("current set is %s" % found_libraries)
    return found_libraries

def updatelibs(args):
    logging.info("Updating libraries...")

    found_libraries = find_current_libraries(args.root)

    release_manager = ReleaseManager()

    unknown_libraries = found_libraries - release_manager.library_set
    known_libraries = found_libraries & release_manager.library_set

    dependencies = release_manager.get_dependencies(known_libraries)

    final_libraries = known_libraries | dependencies

    new_libraries = final_libraries - known_libraries

    if unknown_libraries:
        logging.info('Not updating these unknown libraries: %s' % ', '.join(unknown_libraries))

    if new_libraries:
        logging.info("Installing new libraries: %s" % ", ".join(new_libraries))

    if known_libraries:
        logging.info("Updating existing libraries: %s" % ", ".join(known_libraries))

    # final_libraries has the final list, including new ones from dependencies

    (version, _) = blinka.board.identify(args.root)
    logging.debug("detected board version %s", version)
    version = semver.Version.parse(version)
    logging.debug("major version is %s" % version.major)
    release_manager.get_libraries(version, args.tempdir)

    release_manager.update_or_install_libraries(final_libraries, args.root)

def find_root():
    return blinka.fsutil.find_circuit_python_user_mode_root()

def setup_argument_parser(parser):
    root = find_root()
    parser.description="Updates your CircuitPython libraries to the latest version."
    parser.add_argument("-r", "--root", action="store", dest="root", default=root, help="specify the root directory of your CircuitPython (default: %(default)s)", required=root is None)
    parser.set_defaults(func=updatelibs)
