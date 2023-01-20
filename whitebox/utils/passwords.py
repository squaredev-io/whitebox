from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
from src.core.settings import get_settings


settings = get_settings()


def to_utf8(ps):
    return ps.encode("utf-8")


def encrypt_api_key(password: str, key: bytes) -> str:
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(to_utf8(password)) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return (iv + ct).hex()


def decrypt_api_key(password: str, key: bytes) -> str:
    ct = bytes.fromhex(password)
    iv = ct[:16]
    ct = ct[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(pt) + unpadder.finalize()
    return data.decode("utf-8")


def passwords_match(api_key_in_db: str, api_key_in_headers: str):
    if not settings.SECRET_KEY:
        return api_key_in_db == api_key_in_headers

    api_key = decrypt_api_key(api_key_in_db, settings.SECRET_KEY.encode())
    return api_key == api_key_in_headers
