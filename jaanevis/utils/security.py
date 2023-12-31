import uuid

from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> str:
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False


if __name__ == "__main__":
    _hash = hash_password(uuid.uuid4().hex)
    print(_hash)
