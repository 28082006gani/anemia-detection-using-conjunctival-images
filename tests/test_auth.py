def test_auth_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"AnemiaScan" in response.data
    assert b"Sign in" in response.data
    assert b"Create account" in response.data

def test_user_registration_success(client):
    response = client.post('/register', data={
        'email': 'nurse.test@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account registered successfully" in response.data or b"Dashboard" in response.data
    assert b"nurse.test@clinic.org" in response.data

def test_user_registration_invalid_password(client):
    # Too short (< 4 characters)
    response = client.post('/register', data={
        'email': 'nurse.short@clinic.org',
        'password': 'ab',
        'confirm_password': 'ab'
    }, follow_redirects=True)
    assert response.status_code == 400
    assert b"Password must be at least 4 characters" in response.data

def test_user_registration_duplicate_email(client):
    client.post('/register', data={
        'email': 'duplicate@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    })
    client.post('/logout')
    response = client.post('/register', data={
        'email': 'duplicate@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)
    assert response.status_code == 400
    assert b"already exists" in response.data

def test_login_success_and_logout(client):
    client.post('/register', data={
        'email': 'doctor.who@hospital.org',
        'password': 'SecretPassword99',
        'confirm_password': 'SecretPassword99'
    })
    client.post('/logout')

    # Login
    response = client.post('/login', data={
        'email': 'doctor.who@hospital.org',
        'password': 'SecretPassword99'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"doctor.who@hospital.org" in response.data

    # Logout
    logout_resp = client.post('/logout', follow_redirects=True)
    assert logout_resp.status_code == 200
    assert b"You have been signed out" in logout_resp.data

def test_login_invalid_credentials_generic_message(client):
    response = client.post('/login', data={
        'email': 'nonexistent@clinic.org',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    assert response.status_code == 401
    # Generic error rule from SECURITY.md
    assert b"Email or password is incorrect" in response.data
