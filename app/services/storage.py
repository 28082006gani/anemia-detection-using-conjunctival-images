import os
import uuid
from PIL import Image

def save_uploaded_image(file_storage, upload_folder: str) -> str:
    """
    Re-encodes the image to a standardized JPEG, stripping all EXIF/GPS metadata
    and any embedded non-image payloads.
    Saves with a cryptographically secure random UUID filename.
    """
    os.makedirs(upload_folder, exist_ok=True)
    random_filename = f"{uuid.uuid4().hex}.jpg"
    target_path = os.path.join(upload_folder, random_filename)

    file_storage.seek(0)
    with Image.open(file_storage) as img:
        # Convert to RGB (handles RGBA, Palette, Grayscale)
        rgb_img = img.convert('RGB')
        # Save as clean JPEG without EXIF metadata
        rgb_img.save(target_path, format='JPEG', quality=90, optimize=True)

    return random_filename

def get_image_path(filename: str, upload_folder: str) -> str | None:
    """
    Safely resolves the image file path preventing directory traversal.
    """
    if not filename or '/' in filename or '\\' in filename or '..' in filename:
        return None
    full_path = os.path.join(upload_folder, filename)
    if os.path.isfile(full_path):
        return full_path
    return None

def delete_image_file(filename: str, upload_folder: str) -> bool:
    target_path = get_image_path(filename, upload_folder)
    if target_path and os.path.isfile(target_path):
        try:
            os.remove(target_path)
            return True
        except OSError:
            return False
    return False
