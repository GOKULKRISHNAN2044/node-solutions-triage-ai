import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a unique random salt.
    Zero external dependencies, cross-platform and secure.
    """
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"


def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify password against stored salt$hash.
    """
    try:
        salt, key = stored_hash.split("$", 1)
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return secrets.compare_digest(key, new_key.hex())
    except Exception:
        return False
