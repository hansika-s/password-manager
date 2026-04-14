from passwordmanager import security, storage


def add_credential(service: str, username: str, password: str, key: bytes) -> None:
    vault = storage.load_vault()
    vault[service] = {
        "username": security.encrypt_data(username, key),
        "password": security.encrypt_data(password, key),
    }
    storage.save_vault(vault)


def get_credential(service: str, key: bytes) -> tuple[str, str] | None:
    vault = storage.load_vault()
    creds = vault.get(service)
    if creds is None or service == storage.CANARY_KEY:
        return None
    return (
        security.decrypt_data(creds["username"], key),
        security.decrypt_data(creds["password"], key),
    )


def edit_credential(
    service: str,
    username: str | None,
    password: str | None,
    key: bytes,
) -> bool:
    vault = storage.load_vault()
    if service not in vault or service == storage.CANARY_KEY:
        return False
    if username is not None:
        vault[service]["username"] = security.encrypt_data(username, key)
    if password is not None:
        vault[service]["password"] = security.encrypt_data(password, key)
    storage.save_vault(vault)
    return True


def delete_credential(service: str) -> bool:
    vault = storage.load_vault()
    if service not in vault or service == storage.CANARY_KEY:
        return False
    del vault[service]
    storage.save_vault(vault)
    return True


def list_services() -> list[str]:
    return [k for k in storage.load_vault().keys() if k != storage.CANARY_KEY]
