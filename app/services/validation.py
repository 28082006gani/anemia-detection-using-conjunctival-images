import re
import io
from PIL import Image

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
NAME_REGEX = re.compile(r"^[A-Za-z\s.'-]{2,80}$")

PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
JPEG_MAGIC = b'\xff\xd8\xff'

MAX_IMAGE_DIMENSION = 4000

def validate_registration(email: str, password: str, confirm_password: str = None) -> list[str]:
    errors = []
    email = (email or '').strip()
    password = password or ''
    confirm_password = confirm_password or ''

    if not email:
        errors.append("Email is required.")
    elif not EMAIL_REGEX.match(email):
        errors.append("Please enter a valid email address.")

    if not password:
        errors.append("Password is required.")
    elif len(password) < 4:
        errors.append("Password must be at least 4 characters.")

    if confirm_password and password != confirm_password:
        errors.append("Passwords do not match.")

    return errors

def validate_patient_form(name: str, age: str, place: str) -> tuple[dict, list[str]]:
    errors = []
    cleaned = {}

    name = (name or '').strip()
    if not name:
        errors.append("Patient name is required.")
    elif not NAME_REGEX.match(name):
        errors.append("Name must be 2 to 80 characters and contain only letters, spaces, hyphens, periods, or apostrophes.")
    else:
        cleaned['name'] = name

    age_str = (age or '').strip()
    if not age_str:
        errors.append("Age is required.")
    else:
        try:
            age_int = int(age_str)
            if age_int < 0 or age_int > 120:
                errors.append("Age must be between 0 and 120.")
            else:
                cleaned['age'] = age_int
        except ValueError:
            errors.append("Age must be a valid whole number.")

    place = (place or '').strip()
    if not place:
        errors.append("Place/Location is required.")
    elif len(place) < 2 or len(place) > 120:
        errors.append("Place must be between 2 and 120 characters.")
    elif any(ord(c) < 32 for c in place):
        errors.append("Place cannot contain control characters.")
    else:
        cleaned['place'] = place

    return cleaned, errors

def validate_image_file(file_storage) -> tuple[bool, str]:
    if not file_storage or not file_storage.filename:
        return False, "Please select an eye conjunctiva image to upload."

    filename = file_storage.filename.lower()
    allowed_exts = ('.png', '.jpg', '.jpeg')
    if not any(filename.endswith(ext) for ext in allowed_exts):
        return False, "Image must be PNG or JPG and under 5 MB."

    header = file_storage.read(8)
    file_storage.seek(0)

    is_png = header.startswith(PNG_MAGIC)
    is_jpeg = header.startswith(JPEG_MAGIC)

    if not (is_png or is_jpeg):
        return False, "Invalid image format. Only authentic PNG and JPEG images are allowed."

    try:
        image_bytes = file_storage.read()
        file_storage.seek(0)
        
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.verify()

        with Image.open(io.BytesIO(image_bytes)) as img:
            width, height = img.size
            if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
                return False, f"Image dimensions too large (max {MAX_IMAGE_DIMENSION}x{MAX_IMAGE_DIMENSION}px)."
            if width < 50 or height < 50:
                return False, "Image dimensions are too small for analysis (min 50x50px)."
    except Exception:
        return False, "Corrupted or invalid image file. Please upload a clear photo."

    return True, ""
