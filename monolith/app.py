import os, time
import connexion
from venv import create

from .views import blueprints

os.environ['TZ'] = 'UTC'
time.tzset()

app = None
api_app = None


def create_app():
    """Create the application and setup Connexion."""
    global app
    global api_app

    api_app = connexion.FlaskApp(
        __name__,
        server='flask',
        specification_dir='openapi/',
    )
    register_specifications(api_app)
    app = api_app.app

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


def register_specifications(_api_app):
    """
    This function registers all resources in the flask application
    :param _api_app: Flask Application Object
    :return: None
    """

    # Scan the specifications package and add all yaml files.
    from importlib_resources import files
    
    folder = files('monolith.specifications')
    for _, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = folder.joinpath(file)
                _api_app.add_api(file_path)


app = create_app()
