import os
from flask import Blueprint, Response
from ..models import File


bl = Blueprint('files', __name__)


@bl.route('/<path:filename>')
def media(filename):
    """Serves uploaded files. This view is also used to generate urls to files
    using url_for method. Shouldn't be used in production (override routes to
    this view in your web server configuration and serve the files directly).
    """
    key = os.path.splitext(filename)[0]
    j = File.get(key)
    return Response(j['data'], mimetype=j['mime'])
