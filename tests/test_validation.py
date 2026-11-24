import io
from werkzeug.datastructures import FileStorage
from app.services.validation import validate_patient_form, validate_image_file, validate_registration
from tests.conftest import make_test_image

def test_validate_registration_rules():
    assert len(validate_registration('test@example.com', 'Pass1234', 'Pass1234')) == 0
    assert "Please enter a valid email address." in validate_registration('not-an-email', 'Pass1234', 'Pass1234')
    assert "Password must be at least 4 characters." in validate_registration('t@e.com', 'ab', 'ab')
    assert "Passwords do not match." in validate_registration('t@e.com', 'Pass1234', 'Diff1234')

def test_validate_patient_form_success():
    cleaned, errors = validate_patient_form('Ramesh Kumar', '45', 'Hubballi Central')
    assert len(errors) == 0
    assert cleaned['name'] == 'Ramesh Kumar'
    assert cleaned['age'] == 45
    assert cleaned['place'] == 'Hubballi Central'

def test_validate_patient_form_invalid_inputs():
    # Invalid name (symbols/numbers)
    _, errors = validate_patient_form('John123 <script>', '25', 'Bangalore')
    assert len(errors) > 0

    # Invalid age (out of bounds)
    _, errors = validate_patient_form('John Doe', '150', 'Bangalore')
    assert any("Age must be between 0 and 120" in e for e in errors)

    # Empty place
    _, errors = validate_patient_form('John Doe', '25', '')
    assert any("Place/Location is required" in e for e in errors)

def test_validate_image_file_valid():
    buf = make_test_image(format='JPEG')
    fs = FileStorage(stream=buf, filename='eye.jpg', content_type='image/jpeg')
    valid, err = validate_image_file(fs)
    assert valid is True
    assert err == ""

def test_validate_image_file_rejects_spoofed_text_file():
    fake_buf = io.BytesIO(b"Hello this is a malicious text payload disguised as an image")
    fs = FileStorage(stream=fake_buf, filename='hack.jpg', content_type='image/jpeg')
    valid, err = validate_image_file(fs)
    assert valid is False
    assert "Invalid image format" in err or "Corrupted" in err

def test_validate_image_file_rejects_disallowed_extension():
    buf = make_test_image(format='PNG')
    fs = FileStorage(stream=buf, filename='script.exe', content_type='application/octet-stream')
    valid, err = validate_image_file(fs)
    assert valid is False
    assert "PNG or JPG" in err
