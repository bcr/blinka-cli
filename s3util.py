import logging
# Do some initial logging setup -- this really needs to be here, before you do
# stuff with argparse. Trust me on this.
logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)

# Put in some emojis for fun
emojis = {
    logging.DEBUG       : "\N{Nerd Face}",
    logging.INFO        : "\N{Thumbs Up Sign}",
    logging.WARNING     : "\N{Worried Face}",
    logging.ERROR       : "\N{No Entry}",
    logging.CRITICAL    : "\N{Serious Face With Symbols Covering Mouth}",
}

for emoji in emojis:
    logging.addLevelName(emoji, emojis[emoji])

try:
    import boto3
    from botocore.handlers import disable_signing
except ImportError:
    logging.error(" --commit-hash param will not work without boto3")
def find_firmware_by_hash(hash, board, language):
    resource = boto3.resource('s3')
    resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = resource.Bucket('adafruit-circuit-python')

    for item in bucket.objects.filter(Prefix="bin/{}/{}/".format(board, language)):
        if hash in item.key and ".uf2" in item.key:
            return item.key
    return None