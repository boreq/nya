"""
    Implements basic database related methods. flask-sqlalchemy extension
    provides database support. That extension automatically handles the session
    management and binds it to the request context. Actual database models are
    defined in models.py.
"""


from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db():
    """Creates all defined database tables."""
    db.create_all()


def destroy_db():
    """Drops all defined database tables."""
    db.drop_all()
