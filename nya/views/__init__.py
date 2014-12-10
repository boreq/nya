from . import core, api, files, errors


def register_blueprints(app):
    app.register_blueprint(api.bl, url_prefix='/api')
    app.register_blueprint(core.bl)
    app.register_blueprint(files.bl, url_prefix=app.config['FILES_URL'])
    app.register_blueprint(errors.bl)
