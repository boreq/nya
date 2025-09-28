import os
from flask import Blueprint, Response, abort
from ..models import File


bl = Blueprint('files', __name__)


@bl.route('/<path:filename>')
def media(filename):
    """Serves uploaded files."""
    j = File.get(filename)
    if j is None:
        abort(404)
    return Response(j['data'], mimetype=j['mime'])
