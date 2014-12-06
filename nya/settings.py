"""
    Default settings.

    Path to the custom settings file should be specified in the NYA_SETTINGS
    environment variable. Settings defined there will overwrite values present
    in this file. If you want to run multiple instances of the app with
    different configs you can change the name of the environment variable by
    passing the parameter to the application factory. See the source code in
    __init__.py for more details. To set the environment variable use the export
    command:

        export NYA_SETTINGS=/path/to/custom_settings.py

    Obviously you can modify this file directly but that might cause conflicts
    while updating the repository and it is a good practice to keep the default
    values for reference. Furthermore it would be impossible to easily run
    multiple instances of this app that way and your modification could
    influence unit testing.
"""


# Max cache age.
# Cache is disabled in DEBUG or TESTING mode.
# See cache.Cache._get_preferred_cache_system to learn more.
# [seconds]
CACHE_TIMEOUT = 60 * 5

# Adds prefix to all cache keys. Change this to run multiple instances of this
# app.
CACHE_KEY_PREFIX = 'nya'

# List of memcached servers. Set to None to disable. Should be a tuple
# or a list. Example:
# MEMCACHED = ['127.0.0.1:11211']
MEMCACHED = None

# Redis server. Set to None to disable. Should be a dictionary. Set the
# arguments in the following way:
# REDIS = {'host': 'localhost', 'port': 6379, 'password': None, 'db': 0}
REDIS = None

# Database URI.
# https://pythonhosted.org/Flask-SQLAlchemy/config.html#configuration-keys
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/nya'

# Directory to which the files will be uploaded.
UPLOAD_DIR = '/path/to/directory/'

# Secret key is used by Flask to handle sessions. Set it to random value.
SECRET_KEY = 'dev_key'
