import getpass
import sys

from cryptography.fernet import InvalidToken

from passwordmanager import security, storage

_CANARY_VALUE = "ok"


def unlock_or_setup() -> bytes:
    if not storage.salt_exists():
        return _setup()
    return _unlock()


def _setup() -> bytes:
    print("No vault found. Setting up a new one.")
    while True:
        password = getpass.getpass("Create master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        if password == confirm:
            break
        print("Passwords do not match. Try again.")

    salt = security.generate_salt()
    storage.save_salt(salt)
    key = security.derive_key(password, salt)

    vault = {storage.CANARY_KEY: security.encrypt_data(_CANARY_VALUE, key)}
    storage.save_vault(vault)
    print("Vault created.")
    return key


def _unlock() -> bytes:
    password = getpass.getpass("Enter master password: ")
    salt = storage.load_salt()
    key = security.derive_key(password, salt)

    vault = storage.load_vault()
    canary = vault.get(storage.CANARY_KEY)
    if canary is None:
        print("Vault appears corrupted (missing verification token).")
        sys.exit(1)

    try:
        security.decrypt_data(canary, key)
    except InvalidToken:
        print("Incorrect master password.")
        sys.exit(1)

    return key
