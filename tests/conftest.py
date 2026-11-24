import os
import tempfile
import io
import pytest
from PIL import Image
from app import create_app
from app.models import get_db, init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    upload_dir = tempfile.mkdtemp()

    test_config = {
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'DATABASE_PATH': db_path,
        'UPLOAD_FOLDER': upload_dir,
        'SECRET_KEY': 'test-secret-key-for-testing-only-12345',
        'RATELIMIT_ENABLED': False,
    }

    app = create_app(test_config=test_config)

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def make_test_image(format='JPEG', size=(200, 200), color=(180, 50, 50)):
    buf = io.BytesIO()
    img = Image.new('RGB', size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf
