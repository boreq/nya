import base64
import datetime
import pytz


def utc_now():
    """Get a datetime representing current time in UTC."""
    return pytz.utc.localize(datetime.datetime.utcnow())


def filehash(f, hasher, blocksize=65536):
    """Returns a hash of the file and size of the stream."""
    buf = f.read(blocksize)
    size = 0
    while len(buf) > 0:
        size += len(buf)
        hasher.update(buf)
        buf = f.read(blocksize)
    return (hasher.digest(), size)


def b64_filehash(*args, **kwargs):
    """Generates a file hash and encodes it in base64."""
    rd = filehash(*args, **kwargs)
    return (base64.b64encode(rd[0]).decode(), rd[1])


def hr_size(num, suffix='B'):
    """Return human readable size."""
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f%s%s' % (num, 'Yi', suffix)
