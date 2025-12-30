import os
from cryptography.fernet import Fernet

def generate_key():
    """Generate and save a new encryption key."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load existing encryption key or generate a new one."""
    if not os.path.exists("secret.key"):
        return generate_key()
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypt a string message using the provided key."""
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_data: bytes, key: bytes) -> str:
    """Decrypt bytes data using the provided key."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()