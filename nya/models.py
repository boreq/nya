"""
    flask-sqlalchemy models.
"""


import datetime
import os
from flask import url_for, current_app
from .database import db
from .helpers import utc_now


class File(db.Model):
    __tablename__ = 'nya_files'

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(88), nullable=False)
    size = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now())
    expires = db.Column(db.DateTime(timezone=True), nullable=True, default=None)

    def __str__(self):
        return '<File #%d>' % self.id

    @property
    def filename(self):
        """Returns a filename. Example:
        123.jpg
        """
        return '%d%s' % (self.id, self.extension)

    @property
    def filepath(self): 
        """Returns a path to a file on a hard drive. Example:
        /var/www/upload/nya/123.jpg
        """
        return os.path.join(current_app.config['UPLOAD_DIR'], self.filename)

    @property
    def url(self):
        """Returns an url to a file. See views.files.media. Example:
        /f/123.jpg
        """
        return url_for('files.media', filename=self.filename)

    def to_dict(self):
        """Returns a dictionary which can be easily converted to JSON."""
        properties = ['id', 'original_filename', 'extension', 'hash', 'size', 'url']
        data = {key: getattr(self, key) for key in properties}
        data['date'] = str(self.date)
        data['expires'] = str(self.expires) if self.expires else self.expires
        return data

    def delete_file(self):
        """Deletes a file associated with this database record from a HDD."""
        try:
            os.remove(self.filepath)
        except FileNotFoundError:
            pass

    def set_expiration(self, seconds):
        """Set an expriation date of this file given number of seconds in the
        future.
        """
        self.expires = utc_now() + datetime.timedelta(seconds=seconds)


def pre_file_delete(mapper, connection, target):
    """Deletes the file before deleting the database record."""
    target.delete_file()
db.event.listen(File, 'before_delete', pre_file_delete)
