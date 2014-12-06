"""
    Implements caching.
"""


import re
import hashlib
from functools import wraps
from flask import request, Blueprint
from werkzeug.contrib.cache import MemcachedCache, RedisCache, NullCache


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
        """Call this to init this class with a right cache system."""
        self._client = self._get_preferred_cache_system(app.config)

    def _get_preferred_cache_system(self, config):
        """Returns an initialized cache system object."""
        if config['REDIS']:
            return RedisCache(
                default_timeout=config['CACHE_TIMEOUT'],
                key_prefix=config['CACHE_KEY_PREFIX'],
                **config['REDIS']
            )
        if config['MEMCACHED']:
            return MemcachedCache(
                servers=config['MEMCACHED'],
                default_timeout=config['CACHE_TIMEOUT'],
                key_prefix=config['CACHE_KEY_PREFIX']
            )
        return NullCache()

    __getattr__ = lambda s, n: getattr(s._client, n)


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
        self.dec_kwargs = {
            'timeout': kwargs.pop('timeout', None),
            'key_gen': kwargs.pop('key_gen', None),
        }
        self.dec_kwargs = {key: value for (key, value) in self.dec_kwargs.items() \
                           if value is not None}
        super(CachedBlueprint, self).__init__(*args, **kwargs)

    def add_url_rule(self, *args, **kwargs):
        """Exactly like add_url_rule but adds a cache decorator if desired.

        cached: Indicates whether the view should be cached. Defaults to
                default_cached. Can be used to everride the default setting.
        """
        if kwargs.pop('cached', self.default_cached):
            kwargs['view_func'] = cached(**self.dec_kwargs)(kwargs['view_func'])
        super(CachedBlueprint, self).add_url_rule(*args, **kwargs)
