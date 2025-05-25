from setuptools import setup

setup(
    name='nya',
    version='0.0.0',
    author='boreq',
    author_email='boreq@0x46.net',
    description = ('A simple website for sharing files.'),
    license='BSD',
    packages=['nya'],
    install_requires=[
        'Werkzeug==3.1.3',
        'Flask==3.1.1',
        'Jinja2==3.1.6',
        'click==8.2.1',
        'pytz',
        'redis',
    ],
)
