import datetime
import pytz


def utc_now():
    """Get a datetime representing current time in UTC."""
    return pytz.utc.localize(datetime.datetime.utcnow())


def hr_size(num, suffix='B'):
    """Return human readable size."""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f%s%s' % (num, 'Yi', suffix)
