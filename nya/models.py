import hashlib
import base64
import json
from .cache import cache


def _filehash(f, hasher, blocksize=65536):
    """Returns a hash of the file and size of the stream."""
    buf = f.read(blocksize)
    size = 0
    while len(buf) > 0:
        size += len(buf)
        hasher.update(buf)
        buf = f.read(blocksize)
    return (hasher.hexdigest()[:30], size)


class File(object):

    @staticmethod
    def _transform_key(key):
        return 'file_' + key

    @staticmethod
    def save(file_storage, expires):
        # Create file key
        hasher = hashlib.sha224()
        hash, size = _filehash(file_storage, hasher)
        file_storage.stream.seek(0) # Stream ended after calculating the hash

        # Save the data
        data = {
                'data': base64.b64encode(file_storage.stream.read()).decode(),
                'mime': file_storage.mimetype,
        }
        cache.set(File._transform_key(hash), json.dumps(data), timeout=expires)
        return hash

    @staticmethod
    def get(hash):
        value = cache.get(File._transform_key(hash))
        if value is None:
            return None
        j = json.loads(value)
        j['data'] = base64.b64decode(j['data'])
        return j

    @staticmethod
    def delete(hash):
        cache.delete(File._transform_key(hash))
