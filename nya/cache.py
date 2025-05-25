"""
    Implements caching.
"""


import hashlib
import redis
import pickle
from functools import wraps
from flask import request, Blueprint


_integer_types = (int,)


class Cache(object):
    """Used as an interface to the Werkzeug cache systems. It picks the cache
    system depending on the app configuration.

    app: Flask application object. If not passed you must initialize the
         instance later by calling init_app.
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self._default_timeout = app.config['CACHE_TIMEOUT']
        self._key_prefix = app.config['CACHE_KEY_PREFIX']

        redis_config = app.config['REDIS']
        self._client = redis.Redis(
            host = redis_config['host'],
            port = redis_config['port'],
            password = redis_config['password'],
            db = redis_config['db']
        )
        
    def get(self, key):
        return self._load_object(self._client.get(self._key_prefix + key))

    def set(self, key, value, timeout=None):
        timeout = self._normalize_timeout(timeout)
        dump = self._dump_object(value)
        if timeout == -1:
            result = self._client.set(name=self._key_prefix + key, value=dump)
        else:
            result = self._client.setex(
                name=self._key_prefix + key, value=dump, time=timeout
            )
        return result

    def delete(self, key):
        return self._client.delete(self._key_prefix + key)

    def get_stats(self):
        stats = {}

        info = self._client.info()

        if 'used_memory' in info:
            stats['redis_used_memory'] = info['used_memory']

        if 'used_memory_human' in info:
            stats['redis_used_memory_human'] = info['used_memory_human']

        if 'used_memory_peak' in info:
            stats['redis_peak_memory'] = info['used_memory_peak']

        if 'used_memory_peak_human' in info:
            stats['redis_peak_memory_human'] = info['used_memory_peak_human']

        stats['redis_number_of_keys'] = self._client.dbsize()

        return stats

    def _dump_object(self, value):
        t = type(value)
        if t in _integer_types:
            return str(value).encode("ascii")
        return b"!" + pickle.dumps(value)

    def _load_object(self, value):
        if value is None:
            return None
        if value.startswith(b"!"):
            try:
                return pickle.loads(value[1:])
            except pickle.PickleError:
                return None
        return int(value)

    def _normalize_timeout(self, timeout):
        if timeout is None:
            timeout = self._default_timeout
        if timeout == 0:
            timeout = -1
        return timeout


cache = Cache()


def _get_md5(string):
    """Returns a hash of a string."""
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def get_cache_key(*args, **kwargs):
    """Construct a cache key."""
    return _get_md5(request.full_path)


def cached(timeout=None, key_gen=get_cache_key):
    """Simple cache decorator taken from Flask docs.

    timeout: Cache timeout in seconds. Defaults to the default timeout set for
             the cache system if None.
    key_gen: Function which generates a cache key. This function is called with
             the same parameters as the decorated function.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key_gen(*args, **kwargs)
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator


class CachedBlueprint(Blueprint):
    """Blueprint which automatically adds cached decorator to all views added
    by add_url_rule method.

    timeout: See cached decorator.
    key_gen: See cached decorator.
    default_cached: Indicates whether the views should be cached by default.
    """

    def __init__(self, *args, **kwargs):
        self.default_cached = kwargs.pop('default_cached', True)
        self.cache_options = {
            'timeout': kwargs.pop('timeout', None),
            'key_gen': kwargs.pop('key_gen', None),
        }
        self.cache_options = {key: value for key, value in self.cache_options.items() \
                              if value is not None}
        super(CachedBlueprint, self).__init__(*args, **kwargs)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Exactly like add_url_rule but adds a cache decorator if desired.

        cached: Indicates whether the view should be cached. Defaults to
                default_cached. Can be used to everride the default setting.
        """
        if options.pop('cached', self.default_cached):
            view_func = cached(**self.cache_options)(view_func)
        super(CachedBlueprint, self).add_url_rule(rule, endpoint, view_func, **options)
