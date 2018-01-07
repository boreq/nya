import hashlib
import base64
import json
from .cache import cache


_FILENAME_LENGTH = 30


def _filehash(f, hasher, blocksize=65536):
    """Returns a hash of the file and size of the stream."""
    buf = f.read(blocksize)
    size = 0
    while len(buf) > 0:
        size += len(buf)
        hasher.update(buf)
        buf = f.read(blocksize)
    return (hasher.hexdigest()[:_FILENAME_LENGTH], size)


class File(object):

    @staticmethod
    def save(file_storage, expires):
        # Hash the file
        hasher = hashlib.sha224()
        hash, size = _filehash(file_storage, hasher)
        file_storage.stream.seek(0) # Stream ended after calculating the hash

        # Save the data
        data = {
                'data': file_storage.stream.read(),
                'mime': file_storage.mimetype,
        }
        cache.set(File._transform_key(hash), File._serialize_data(data), timeout=expires)
        return hash

    @staticmethod
    def get(hash):
        data = cache.get(File._transform_key(hash))
        if data is None:
            return None
        return File._deserialize_data(data)

    @staticmethod
    def delete(hash):
        cache.delete(File._transform_key(hash))

    @staticmethod
    def _serialize_data(data):
        data['data'] = base64.b64encode(data['data']).decode()
        return json.dumps(data)

    @staticmethod
    def _deserialize_data(data):
        data = json.loads(data)
        data['data'] = base64.b64decode(data['data'])
        return data

    @staticmethod
    def _transform_key(key):
        return 'file_' + key
