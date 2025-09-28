import hashlib
import base64
import io
import json
import os
from PIL import Image, ImageOps
from .cache import cache


_FILENAME_LENGTH = 30


class File(object):

    @staticmethod
    def save(file_storage, expires):
        data, extension, mime = File._strip_metadata(file_storage)

        hasher = hashlib.sha224()
        hasher.update(data)
        hash = hasher.hexdigest()[:_FILENAME_LENGTH]

        filename = hash + extension

        data = {
                'data': data,
                'filename': filename,
                'mime': mime,
        }
        cache.set(File._transform_key(filename), File._serialize_data(data), timeout=expires)
        return data

    @staticmethod
    def get(filename):
        data = cache.get(File._transform_key(filename))
        if data is None:
            return None
        return File._deserialize_data(data)

    @staticmethod
    def delete(filename):
        cache.delete(File._transform_key(filename))

    @staticmethod
    def _strip_metadata(file_storage):
        data = file_storage.stream.read()

        match file_storage.mimetype:
            case 'image/jpeg':
                img = Image.open(io.BytesIO(data))
                img = ImageOps.exif_transpose(img)

                img_no_exif = Image.new(img.mode, img.size)
                img_no_exif.putdata(list(img.getdata()))

                b = io.BytesIO()
                img_no_exif.save(b, "JPEG", quality=95)
                return b.getvalue(), '.jpg', 'image/jpeg'
            case _:
                extension = os.path.splitext(file_storage.filename)[1]
                mime = file_storage.mimetype
                return data, extension, mime

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
    def _transform_key(filename):
        hasher = hashlib.sha224()
        hasher.update(filename.encode('utf-8'))
        key = hasher.hexdigest()
        return 'file_' + key
