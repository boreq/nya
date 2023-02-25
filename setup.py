from setuptools import setup

setup(
    name='nya',
    version='0.0.0',
    author='boreq',
    author_email='boreq@sourcedrops.com',
    description = ('A simple website for sharing files.'),
    license='BSD',
    packages=['nya'],
    install_requires=[
        'Werkzeug==0.11.3',
        'Flask==0.12.4',
        'Jinja2==2.4',
        'itsdangerous==0.21',
        'click==2.0',
        'pytz',
    ],
    extras_require = {
        'Memcached caching':  ['python3-memcached'],
        'Redis caching':  ['redis'],
    }
)
