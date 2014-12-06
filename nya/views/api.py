import hashlib
import json
import os
from flask import Blueprint, Response, request, current_app
from flask.views import View
from werkzeug import secure_filename
from .. import helpers
from ..cache import CachedBlueprint
from ..database import db
from ..models import File


bl = CachedBlueprint('api', __name__, default_cached=False)


class ApiError(Exception):
    """Base class for all api exceptions."""

    status_code = 500
    error_code = 'unknown'
    message = 'Unknown server error.'

    def __init__(self, **kwargs):
        for name in ['status_code', 'error_code', 'message']:
            if kwargs.get(name, None) is not None:
                setattr(self, name, kwargs[name])
        self.add_data = kwargs.get('add_data', {}) # Additional data, should be dict
        super(ApiError, self).__init__(self.message)


class NotImplementedApiError(ApiError):
    status_code = 501
    error_code = 'not_implemented'
    message = 'Not implemented.'


class MethodNotAllowedApiError(ApiError):
    status_code = 405
    error_code = 'method_not_allowed'
    message = 'Method not allowed.'


class BadRequestApiError(ApiError):
    status_code = 400
    error_code = 'bad_request'
    message = 'Bad request.'


class NotFoundApiError(ApiError):
    status_code = 404
    error_code = 'not_found'
    message = 'Not found.'


class ApiView(View):
    """Base api view. It automatically calls the function named
    <method>_api_response, e.g.: get_api_response.
    """

    methods = ['GET']

    def handle_exception(self, exception):
        """Converts an exception to a tuple containing a HTTP status code and
        response data."""
        response_data = {
            'error_code': exception.error_code,
            'message': exception.message,
        }
        response_data.update(exception.add_data)
        return (response_data, exception.status_code)

    def dispatch_request(self, *args, **kwargs):
        """Executes the right method and handles the exceptions."""
        try:
            attr_name = request.method.lower() + '_api_response'
            if not request.method in self.methods:
                raise MethodNotAllowedApiError
            if not hasattr(self, attr_name):
                raise NotImplementedApiError
            response_data = getattr(self, attr_name)(*args, **kwargs)
            status_code = 200

        except Exception as e:
            # Use the base exception class for exceptions which were not thrown
            # on purpose
            if not isinstance(e, ApiError):
                e = ApiError()
            response_data, status_code = self.handle_exception(e)

        return Response(json.dumps(response_data, indent=4),
            mimetype='application/json',
            status=status_code
        )


class Upload(ApiView):

    methods = ['POST']

    def make_db_entry(self, file_storage):
        """Returns a File database model constructed using FileStorage data."""
        hasher = hashlib.sha512()
        hash, size = helpers.b64_filehash(file_storage, hasher)
        file_storage.stream.seek(0) # Stream ended after calculating the hash
        rw = File(original_filename=file_storage.filename,
                  extension=os.path.splitext(file_storage.filename)[1],
                  hash=hash, size=size)
        try:
            if 'expires' in request.form and request.form['expires']:
                rw.set_expiration(request.form['expires'])
        except:
            raise BadRequestApiError(message='Parameter `expires` should be an '
                'integer containing a number of seconds.')
        return rw

    def add_or_get_file(self, file_storage):
        """Saves the file and returns its database record or returns a record of
        an identical file which already exists.
        """
        file_record = self.make_db_entry(file_storage)

        # Check if the file exists
        record = File.query.filter(File.hash == file_record.hash,
                                   File.expires == file_record.expires) \
                           .first()
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

    def post_api_response(self):
        response = {'files': []}
        try:
            for f in request.files.getlist('file'):
                file_record = self.add_or_get_file(f)
                response['files'].append(file_record.to_dict())
        except:
            # Include the data about the files which were saved in the exception
            raise ApiError(add_data=response)
        return response


class Info(ApiView):

    methods = ['GET']

    def get_api_response(self):
        try:
            id = int(request.args['id'])
        except:
            raise BadRequestApiError(message='Missing or invalid `id` parameter.')
        file_record = File.query.filter(File.id==id).first()
        if file_record is None:
            raise NotFoundApiError
        return {'files': [file_record.to_dict()]}


def get_stats():
    data = db.session.query(db.func.count(File.id).label('total_files'),
                            db.func.sum(File.size).label('total_size')).first()
    return {
        'total_files': data.total_files,
        'total_size': data.total_size
    }


class Stats(ApiView):

    methods = ['GET']

    def get_api_response(self):
        return get_stats()


bl.add_url_rule('/file/upload/', view_func=Upload.as_view('upload'))
bl.add_url_rule('/file/info/', view_func=Info.as_view('info'), cached=True)
bl.add_url_rule('/stats/', view_func=Stats.as_view('stats'), cached=True)
