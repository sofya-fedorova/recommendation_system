import hashlib


def hash_password(password):
    """Хэширует пароль с использованием SHA-256."""
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    return hashed_password


def verify_hashed_password(stored_hash, provided_password):
    """Проверяет, совпадает ли введённый пароль с захэшированной версией."""
    hashed_provided_password = hash_password(provided_password)
    return hashed_provided_password == stored_hash


def checkPassword(password):
    stored_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    provided_password = password

    if verify_hashed_password(stored_hash, provided_password):
        return 1
    else:
        return 0
