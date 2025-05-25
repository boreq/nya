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


# Default cache timeout.
# Cache is disabled in DEBUG or TESTING mode.
# See cache.Cache._get_preferred_cache_system to learn more.
# [seconds]
CACHE_TIMEOUT = 60 * 5

# This is the max age of the uploaded files.
# [seconds]
MAX_EXPIRATION = 60 * 5

# Max file size.
# [bytes]
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Adds prefix to all cache keys. Change this to run multiple instances of this
# app.
CACHE_KEY_PREFIX = 'nya'

# Valkey server. Should be a dictionary. Set the arguments in the following
# way:
# VALKEY = {'host': 'localhost', 'port': 6379, 'password': None, 'db': 0}
VALKEY = None

# Urls to uploaded files are generated with that prefix. For example an url to
# a file '123.jpg' with this option set to '/media' would be:
# /media/123.jpg
FILES_URL = '/f'

# Secret key is used by Flask to handle sessions. Set it to random value.
SECRET_KEY = 'dev_key'
