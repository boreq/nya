"""
    Commands defined here can be used by executing the following in your shell:

        flask --app=/path/to/nya_app.py command_name

    More info: http://flask.pocoo.org/docs/dev/cli/
"""


from flask.cli import AppGroup
from .database import db, init_db, destroy_db
from .helpers import utc_now
from .models import File


cli = AppGroup(__name__)


@cli.command()
def db_init():
    """Crate database tables."""
    init_db()


@cli.command()
def db_destroy():
    """Drop database tables."""
    destroy_db()


@cli.command()
def remove_expired():
    """Remove files which passed their expiration date."""
    files = File.query.filter(File.expires < utc_now()).all()
    # Bulk delete will not trigger Python based cascades. That in effect would
    # leave orphaned files on the hard drive. That is why we need to delete each
    # record seperately
    for f in files:
        db.session.delete(f)
        db.session.commit()
