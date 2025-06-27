# app/utils/license_key_generator.py
import hashlib
import hmac
import base64
from datetime import datetime

from app.core.config import settings

def convert_to_hashed_license_key(
    data_for_key: str,
) -> str:
    hasher = hashlib.sha256()
    hasher.update(data_for_key.encode('utf-8'))
    hashed_data = hasher.digest()

    # Base64 URL-safe encoding for the key, removing padding '='
    encoded_key = base64.urlsafe_b64encode(hashed_data).decode('utf-8').rstrip('=')
    
    return encoded_key

def verify_secure_license_key_hmac(
    full_license_key: str,
    original_data_for_key: str # The *exact* data string used during generation for this key
) -> bool:
    """
    Verifies if an HMAC-signed license key is valid and untampered.
    """
    if not settings.SECRET_KEY or not settings.ALGORITHM:
        raise ValueError("License key verification settings are not configured.")

    parts = full_license_key.split('-', 1)
    if len(parts) != 2:
        return False

    random_part, received_signature = parts

    # Reconstruct the message that was originally signed during generation
    message_to_verify = f"{random_part}-{original_data_for_key}"

    secret_bytes = settings.SECRET_KEY.encode('utf-8')
    message_bytes = message_to_verify.encode('utf-8')

    try:
        hash_func = getattr(hashlib, settings.ALGORITHM.lower())
    except AttributeError:
        raise ValueError(f"Unsupported hash algorithm: {settings.ALGORITHM}. Choose from hashlib.")

    expected_signer = hmac.new(secret_bytes, message_bytes, hash_func)
    expected_signature = expected_signer.hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)