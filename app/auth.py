import hashlib


def get_password_hash(password: str) -> str:
    """Hash the password using MD5 """
    if not password:
        raise ValueError("Password cannot be empty")

    if isinstance(password, bytes):
        password = password.decode("utf-8", errors="ignore")

    hashed = hashlib.md5(password.encode("utf-8")).hexdigest()
    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against an MD5 hash."""
    if isinstance(plain_password, bytes):
        plain_password = plain_password.decode("utf-8", errors="ignore")

    return hashlib.md5(plain_password.encode("utf-8")).hexdigest() == hashed_password
