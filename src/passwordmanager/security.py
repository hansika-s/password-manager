import base64
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt_data(data: str, key: bytes) -> str:
    return Fernet(key).encrypt(data.encode()).decode()


def decrypt_data(token: str, key: bytes) -> str:
    return Fernet(key).decrypt(token.encode()).decode()


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible encryption key from a master password.

    Uses PBKDF2-HMAC-SHA256 with 600,000 iterations. The derived 32-byte
    key is base64-url-encoded to match Fernet's expected key format.
    """
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


def generate_salt() -> bytes:
    return secrets.token_bytes(16)
