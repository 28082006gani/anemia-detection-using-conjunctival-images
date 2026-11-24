from werkzeug.datastructures import FileStorage
from tests.conftest import make_test_image

def test_unauthenticated_user_redirected(client):
    # Cannot access dashboard
    resp = client.get('/dashboard')
    assert resp.status_code == 302
    assert resp.headers['Location'].endswith('/')

    # Cannot view report
    resp = client.get('/report/some-random-id')
    assert resp.status_code == 302

    # Cannot access image
    resp = client.get('/report/some-random-id/image')
    assert resp.status_code == 302

def test_user_a_cannot_access_user_b_report(client):
    # Register and login User A
    client.post('/register', data={
        'email': 'user.a@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    })

    # User A creates a scan
    img_buf = make_test_image(format='JPEG')
    fs = FileStorage(stream=img_buf, filename='eye_a.jpg', content_type='image/jpeg')

    scan_resp = client.post('/scan', data={
        'patient_name': 'Patient Alpha',
        'patient_age': '30',
        'patient_place': 'Ward 1',
        'image': fs
    }, follow_redirects=False)
    assert scan_resp.status_code == 302
    scan_id = scan_resp.headers['Location'].split('scan_id=')[1]

    # User A can view own report and image
    report_resp = client.get(f'/report/{scan_id}')
    assert report_resp.status_code == 200
    assert b"Patient Alpha" in report_resp.data

    image_resp = client.get(f'/report/{scan_id}/image')
    assert image_resp.status_code == 200
    assert image_resp.content_type == 'image/jpeg'

    # User A logs out
    client.post('/logout')

    # Register and login User B
    client.post('/register', data={
        'email': 'user.b@clinic.org',
        'password': 'Password456',
        'confirm_password': 'Password456'
    })

    # User B attempts to access User A's report -> MUST BE 404 (Security rule)
    unauthorized_report = client.get(f'/report/{scan_id}')
    assert unauthorized_report.status_code == 404

    # User B attempts to access User A's image -> MUST BE 404
    unauthorized_image = client.get(f'/report/{scan_id}/image')
    assert unauthorized_image.status_code == 404

    # User B attempts to delete User A's report -> MUST BE 404
    unauthorized_delete = client.post(f'/report/{scan_id}/delete')
    assert unauthorized_delete.status_code == 404

def test_user_can_delete_own_report(client):
    client.post('/register', data={
        'email': 'user.delete@clinic.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    })

    img_buf = make_test_image(format='PNG')
    fs = FileStorage(stream=img_buf, filename='eye_del.png', content_type='image/png')
    scan_resp = client.post('/scan', data={
        'patient_name': 'Patient ToDelete',
        'patient_age': '40',
        'patient_place': 'Ward 2',
        'image': fs
    })
    scan_id = scan_resp.headers['Location'].split('scan_id=')[1]

    # Delete own report
    del_resp = client.post(f'/report/{scan_id}/delete', follow_redirects=True)
    assert del_resp.status_code == 200
    assert b"Report and associated conjunctival image deleted permanently" in del_resp.data

    # Querying deleted report returns 404
    assert client.get(f'/report/{scan_id}').status_code == 404
    assert client.get(f'/report/{scan_id}/image').status_code == 404
