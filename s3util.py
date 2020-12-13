import boto3
from botocore.handlers import disable_signing
import logging

def find_firmware_by_hash(hash, board, language):
    resource = boto3.resource('s3')
    resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = resource.Bucket('adafruit-circuit-python')

    for item in bucket.objects.filter(Prefix="bin/{}/{}/".format(board, language)):
        if hash in item.key and ".uf2" in item.key:
            return item.key
    return None
