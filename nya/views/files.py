from flask import Blueprint, current_app, send_from_directory


bl = Blueprint('files', __name__)


@bl.route('/f/<path:filename>')
def media(filename):
    """Serves uploaded files. This view is also used to generate urls to files
    using url_for method. Shouldn't be used in production (override routes to
    this view in your web server configuration and serve the files directly).
    """
    return send_from_directory(current_app.config['UPLOAD_DIR'], filename)
