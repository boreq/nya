# Nya
A simple website for uploading files.

## Just use docker

This README is outdated, if for some reason you want to run this software: just
use Docker. This will hopefully minimize the amount of computer-induced
suffering you will experience. Reference `compose.dev.yaml`.

## How to install
I recommend using [virtualenv][virtualenv].

    cd cloned_nya_repository
    pip install ./


## How to test it
If you just want to check things out you can run the Flask development server,
but you should not use it for deployment as it is unsafe. You have to go through
configuration step first.

    cd cloned_nya_repository
    FLASK_APP=nya_app.py flask run


## How to deploy
[Official Flask deployment documentation][flask_deploy].  
An object which should be passed to your WSGI server is created in `nya_app.py`
and called `app` so you will probably have to use something like this in your
config:

    nya_app:app


## Configuration
Read comments in `nya/__init__.py` and `nya/settings.py`. To keep it short:
you need to specify the path to the file similar to `nya/settings.py` in
environment variable called `NYA_SETTINGS`.

Valkey is needed to run the website. 


[virtualenv]: https://virtualenv.pypa.io/en/latest/
[flask_deploy]: http://flask.pocoo.org/docs/dev/deploying/
