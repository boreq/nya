from functools import wraps
import os
from flask import request, current_app, url_for
from flask.json import jsonify
from ..cache import CachedBlueprint
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


def add_file(file_storage, expires):
    hash = File.save(file_storage, expires)

    extension = os.path.splitext(file_storage.filename)[1]
    filename = hash + extension

    return {
        'original_filename': file_storage.filename,
        'filename': filename,
        'url': url_for('files.media', filename=filename),
        'expires': expires,
    }


@bl.route('/file/upload', methods=['POST'])
@api_view
def upload():
    expires = request.form.get('expires', -1, type=int)
    if expires < 0:
        raise BadRequest(message='Parameter `expires` should be a non-negative integer.')
    expires = min(current_app.config['MAX_EXPIRATION'], expires)
    rw = {'files': []}
    try:
        for f in request.files.getlist('file'):
            json = add_file(f, expires)
            rw['files'].append(json)
    except:
        raise APIException(data=rw)
    return jsonify(rw)
