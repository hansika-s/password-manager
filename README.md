# Password Manager CLI

A Python CLI password manager with master-password-derived encryption. Built with [Typer](https://typer.tiangolo.com/) and the [`cryptography`](https://cryptography.io/) library.

## Install

```bash
pip install -e .
```

This installs the `pm` command into your active environment.

## Usage

```bash
pm services                          # list stored services
pm add SERVICE USERNAME PASSWORD     # add credentials
pm get SERVICE                       # retrieve credentials
pm edit SERVICE [-u USERNAME] [-p PASSWORD]
pm delete SERVICE                    # remove credentials
```

On the first run, `pm` prompts you to create a master password. Subsequent runs prompt for it before any command. Forgetting the master password is unrecoverable — there is no reset, by design.

## Project structure

```
password-manager/
├── pyproject.toml         # project metadata, dependencies, `pm` entry point
├── README.md
├── src/
│   └── passwordmanager/
│       ├── cli.py         # command-line interface (Typer commands)
│       ├── auth.py        # master password setup and unlock flow
│       ├── vault.py       # credential management (add, get, edit, delete, list)
│       ├── storage.py     # reads and writes vault.json / vault.salt
│       └── security.py    # encryption and key derivation primitives
└── tests/                 # unit tests (work in progress)
```

## Security model

- The master password is never stored. On every run it is prompted via `getpass` and used to derive a Fernet encryption key via PBKDF2-HMAC-SHA256 with 600,000 iterations and a per-vault random salt (`vault.salt`).
- Credentials (both username and password) are encrypted with Fernet before being written to `vault.json`.
- Authentication happens by attempting to decrypt a canary token embedded in the vault. A wrong master password is rejected.

## Requirements

- Python 3.13+
