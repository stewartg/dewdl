from __future__ import annotations

import json
from base64 import b64encode
from pathlib import Path

from appdirs import user_config_dir  # type: ignore


class DewDLConfigs:

    CONFIG_FILE_NAME = "dewdl.json"
    USER_JSON_KEY = "user"
    PASSWORD_JSON_KEY = "password"
    CERT_JSON_KEY = "crt"
    KEY_JSON_KEY = "key"

    _settings_dict: dict = {}
    _cached_state: dict = {}

    @staticmethod
    def load_config_file():
        config_file = DewDLConfigs.config_file_path()
        if not config_file.exists():
            config_file.write_text("{}")

        DewDLConfigs._settings_dict = json.loads(config_file.read_text())

    @staticmethod
    def config_file_path() -> Path:
        return Path(user_config_dir(), DewDLConfigs.CONFIG_FILE_NAME)

    @staticmethod
    def save_config_file():
        config_file = Path(user_config_dir(), DewDLConfigs.CONFIG_FILE_NAME)
        config_file.write_text(json.dumps(DewDLConfigs._settings_dict))

    @staticmethod
    def update_user(user_name: str):
        DewDLConfigs._settings_dict[DewDLConfigs.USER_JSON_KEY] = user_name
        DewDLConfigs.save_config_file()

    @staticmethod
    def update_password(password: str):
        parsed_password = password
        if password.startswith('"') and password.endswith('"'):
            parsed_password = password[1:-1]
        elif password.startswith("'") and password.endswith("'"):
            parsed_password = password[1:-1]

        DewDLConfigs._settings_dict[DewDLConfigs.PASSWORD_JSON_KEY] = parsed_password
        DewDLConfigs.save_config_file()

    @staticmethod
    def update_crt_path(cert_path: Path):
        DewDLConfigs._settings_dict[DewDLConfigs.CERT_JSON_KEY] = cert_path.as_posix()
        DewDLConfigs.save_config_file()

    @staticmethod
    def update_key_path(key_path: Path):
        DewDLConfigs._settings_dict[DewDLConfigs.KEY_JSON_KEY] = key_path.as_posix()
        DewDLConfigs.save_config_file()

    @staticmethod
    def get_user() -> str | None:
        return DewDLConfigs._settings_dict.get(DewDLConfigs.USER_JSON_KEY)

    @staticmethod
    def get_password() -> str | None:
        return DewDLConfigs._settings_dict.get(DewDLConfigs.PASSWORD_JSON_KEY)

    @staticmethod
    def get_crt_path() -> Path | None:
        cert_path = DewDLConfigs._settings_dict.get(DewDLConfigs.CERT_JSON_KEY)
        if cert_path is not None:
            cert_path = Path(cert_path)
        return cert_path

    @staticmethod
    def get_key_path() -> Path | None:
        key_path = DewDLConfigs._settings_dict.get(DewDLConfigs.KEY_JSON_KEY)
        if key_path is not None:
            key_path = Path(key_path)
        return key_path

    @staticmethod
    def delete_user():
        DewDLConfigs._settings_dict.pop(DewDLConfigs.USER_JSON_KEY)
        DewDLConfigs.save_config_file()

    @staticmethod
    def delete_password():
        DewDLConfigs._settings_dict.pop(DewDLConfigs.PASSWORD_JSON_KEY)
        DewDLConfigs.save_config_file()

    @staticmethod
    def delete_crt_path():
        DewDLConfigs._settings_dict.pop(DewDLConfigs.CERT_JSON_KEY)
        DewDLConfigs.save_config_file()

    @staticmethod
    def delete_key_path():
        DewDLConfigs._settings_dict.pop(DewDLConfigs.KEY_JSON_KEY)
        DewDLConfigs.save_config_file()

    @staticmethod
    def get_b64_key() -> str:

        user = DewDLConfigs.get_user()
        password = DewDLConfigs.get_password()
        if user is None:
            raise ValueError("User name is not set. Run 'dewdl config user <your-user>' and try again.")

        if password is None:
            raise ValueError("Password is not set. Run 'dewdl config password <your-password>' and try again.")

        key = ":".join([user, password])
        return " ".join(["Basic", b64encode(key.encode("utf-8")).decode("ascii")])

    @staticmethod
    def cache_state():
        DewDLConfigs._cached_state = DewDLConfigs._settings_dict.copy()

    @staticmethod
    def restore_state():
        DewDLConfigs._settings_dict = DewDLConfigs._cached_state.copy()
        DewDLConfigs.save_config_file()

    @staticmethod
    def debug():
        print(f"Config Path: {DewDLConfigs.config_file_path()}")
        print(f"User: {DewDLConfigs.get_user()}")
        print(f"Password: {DewDLConfigs.get_password()}")
        print(f"CRT Path: {DewDLConfigs.get_crt_path()}")
        print(f"Key Path: {DewDLConfigs.get_key_path()}")
