from setuptools import setup

setup(
    name='nya',
    version='0.0.0',
    author='boreq',
    author_email='boreq@sourcedrops.com',
    description = ('Simple website for sharing files.'),
    license='BSD',
    packages=['nya'],
    install_requires=[
        'Werkzeug>=0.10',
        'Flask>=0.11',
        'flask-sqlalchemy',
        'pytz',
        'click',
    ],
    extras_require = {
        'Memcached caching':  ['python3-memcached'],
        'Redis caching':  ['redis'],
        'PostgreSQL':  ['psycopg2'],
    }
)
