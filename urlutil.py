import json
import logging
import os.path
import urllib.request
from urllib.parse import urlparse
try:
    import boto3
    from botocore.handlers import disable_signing
except ImportError:
    logging.warn("commit hash param will not work without boto3")

def get_json_from_url(url):
    with urllib.request.urlopen(url) as stream:
        return json.loads(stream.read().decode())

def get_local_file_from_url(url, tempdir):
    # Figure out the filename and pathname
    (_, filename) = os.path.split(urlparse(url).path)
    pathname = os.path.join(tempdir, filename)
    logging.debug("filename is %s" % filename)

    logging.debug("retrieving %s and putting it in %s" % (url, pathname))
    # urllib.request.urlretrieve(url, pathname)

    # https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    # If you don't change the User-Agent you will get a 403
    request = urllib.request.Request(url, headers={'User-Agent': 'Blinka CLI'})

    with urllib.request.urlopen(request) as stream:
        with open(pathname, "wb") as output:
            output.write(stream.read())

    return pathname

def find_firmware_by_hash(hash, board, language):
    resource = boto3.resource('s3')
    resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = resource.Bucket('adafruit-circuit-python')

    for item in bucket.objects.filter(Prefix="bin/{}/{}/".format(board, language)):
        if hash in item.key and ".uf2" in item.key:
            return item.key
    return None


def get_s3_url(s3_path):
    BASE_URL = 'https://adafruit-circuit-python.s3.amazonaws.com/{}'
    return BASE_URL.format(s3_path)