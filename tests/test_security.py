import io
import pytest
from app import create_app
from tests.conftest import make_test_image
from werkzeug.datastructures import FileStorage

def test_security_headers_present(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['X-Frame-Options'] == 'DENY'
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['Referrer-Policy'] == 'no-referrer'
    assert "default-src 'self'" in response.headers['Content-Security-Policy']

def test_cache_control_on_authenticated_views(client):
    client.post('/register', data={
        'email': 'cache.test@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    })
    dashboard_resp = client.get('/dashboard')
    assert dashboard_resp.status_code == 200
    assert 'no-store' in dashboard_resp.headers.get('Cache-Control', '')

def test_csrf_protection_blocks_post_when_enabled():
    app = create_app(test_config={
        'TESTING': True,
        'WTF_CSRF_ENABLED': True,
        'SECRET_KEY': 'csrf-test-secret',
        'RATELIMIT_ENABLED': False,
    })
    csrf_client = app.test_client()

    # POST without CSRF token must be rejected (400 Bad Request)
    resp = csrf_client.post('/login', data={
        'email': 'hacker@clinic.org',
        'password': 'Password123'
    })
    assert resp.status_code == 400

def test_file_size_exceeding_limit_rejected(app, client):
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024  # 100 KB test limit
    client.post('/register', data={
        'email': 'large.file@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    })

    # Create oversized dummy data (200 KB)
    big_data = io.BytesIO(b'x' * (200 * 1024))
    fs = FileStorage(stream=big_data, filename='big.jpg', content_type='image/jpeg')

    resp = client.post('/scan', data={
        'patient_name': 'Test Large',
        'patient_age': '30',
        'patient_place': 'Test Place',
        'image': fs
    })
    assert resp.status_code == 413
