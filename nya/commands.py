"""
    Commands defined here can be used by executing the following in your shell:

        flask --app=/path/to/nya_app.py command_name

    More info: http://flask.pocoo.org/docs/dev/cli/
"""


import click
from flask.cli import AppGroup
from .models import File


cli = AppGroup(__name__)


@cli.command()
@click.argument('hash', type=click.STRING)
def remove(hash):
    """Remove a file."""
    File.delete(hash)
