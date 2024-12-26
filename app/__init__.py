from flask import Flask
from config import config
import os

def create_app(config_name='default'):
    # Create Flask app with explicit template and static folders
    app_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.dirname(app_dir)
    template_dir = os.path.join(project_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)
    
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app 