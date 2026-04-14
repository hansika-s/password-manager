import json
import os

VAULT_FILE = "vault.json"
SALT_FILE = "vault.salt"
CANARY_KEY = "__verify__"


def vault_exists() -> bool:
    return os.path.exists(VAULT_FILE)


def salt_exists() -> bool:
    return os.path.exists(SALT_FILE)


def load_vault() -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(vault: dict) -> None:
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)


def load_salt() -> bytes:
    with open(SALT_FILE, "rb") as f:
        return f.read()


def save_salt(salt: bytes) -> None:
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
