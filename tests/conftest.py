import os
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create the app with testing config
    app = create_app('testing')
    
    # Create test upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    yield app
    
    # Clean up: remove test upload directory
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        os.rmdir(app.config['UPLOAD_FOLDER'])

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner() 