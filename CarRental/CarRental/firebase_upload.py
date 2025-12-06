from firebase_admin import storage
import uuid

def upload_file_to_firebase(file, folder="uploads"):
    bucket = storage.bucket()

    unique_name = f"{folder}/{uuid.uuid4()}_{file.name}"

    blob = bucket.blob(unique_name)
    blob.upload_from_file(file, content_type=file.content_type)

    blob.make_public()

    return blob.public_url
