from functools import wraps
import hashlib
import os
from flask import request, current_app
from flask.json import jsonify
from .. import helpers
from ..cache import CachedBlueprint
from ..database import db
from ..models import File


bl = CachedBlueprint('api', __name__, default_cached=False)


class APIException(Exception):
    """Base API exception.

    message: human readable message.
    status_code: HTTP status code.
    data: dictionary with additional data to display.
    """
    status_code = 500
    message = 'Unknown API error.'

    def __init__(self, message=None, status_code=None, data=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.data = data

    def to_dict(self):
        rv = {'message': self.message}
        if self.data is not None:
            rv.update(self.data)
        return rv


class BadRequest(APIException):
    status_code = 400
    message = 'Bad request.'


class NotFound(APIException):
    status_code = 404
    message = 'Not found.'


def api_view(f):
    """Decorator which catches exceptions which don't inherit from APIException 
    and throws an APIException instead. That way a wrapped view will always
    trigger the api error handler instead of the main one.
    """
    @wraps(f)
    def df(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIException:
            raise
        except Exception:
            raise APIException
    return df


@bl.app_errorhandler(APIException)
def api_exc_handler(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


def make_db_entry(file_storage, expires):
    """Returns a File database model constructed using FileStorage data."""
    hasher = hashlib.sha512()
    hash, size = helpers.b64_filehash(file_storage, hasher)
    file_storage.stream.seek(0) # Stream ended after calculating the hash
    rw = File(original_filename=file_storage.filename,
              extension=os.path.splitext(file_storage.filename)[1],
              hash=hash, size=size)
    if expires > 0:
        rw.set_expiration(expires)
    return rw


def add_or_get_file(file_storage, expires):
    """Saves the file and returns its database record or returns a record of
    an identical file if it already exists.
    """
    file_record = make_db_entry(file_storage, expires)

    # Check if the file exists
    record = File.query.filter(File.hash == file_record.hash,
                               File.expires == file_record.expires).first()
    if record:
        return record

    # Otherwise create a new file
    db.session.add(file_record)
    db.session.flush()
    db.session.refresh(file_record)
    path = os.path.join(current_app.config['UPLOAD_DIR'], file_record.filename)
    file_storage.save(path)
    db.session.commit()
    return file_record


def get_stats():
    """Get stats about the uploaded files."""
    data = db.session.query(db.func.count(File.id).label('total_files'),
                            db.func.sum(File.size).label('total_size')).first()
    return {
        'total_files': data.total_files,
        'total_size': data.total_size or 0 # Avoid returning null instead of 0
    }


@bl.route('/file/upload', methods=['POST'])
@api_view
def upload():
    expires = request.form.get('expires', -1, type=int)
    if expires < 0:
        raise BadRequest(message='Parameter `expires` should be a non-negative '
            'integer.')
    rw = {'files': []}
    try:
        for f in request.files.getlist('file'):
            file_record = add_or_get_file(f, expires)
            rw['files'].append(file_record.to_dict())
    except:
        raise APIException(data=rw)
    return jsonify(rw)


@bl.route('/file/info', cached=True)
@api_view
def info():
    id = request.args.get('id', -1, type=int)
    if id < 0:
        raise BadRequest(message='Id is missing or invalid.')
    file_record = File.query.filter(File.id == id).first()
    if file_record is None:
        raise NotFound(message='No file with such id.')
    return jsonify({'files': [file_record.to_dict()]})


@bl.route('/stats', cached=True)
@api_view
def stats():
    return jsonify(get_stats())
