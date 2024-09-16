from pathlib import Path

from dewdl import DewDLConfigs


def set_config(config_key: str, config_value: str):

    if config_key == DewDLConfigs.USER_JSON_KEY:
        DewDLConfigs.update_user(config_value)
    elif config_key == DewDLConfigs.PASSWORD_JSON_KEY:
        DewDLConfigs.update_password(config_value)
    elif config_key == DewDLConfigs.CERT_JSON_KEY:
        DewDLConfigs.update_crt_path(Path(config_value))
    elif config_key == DewDLConfigs.KEY_JSON_KEY:
        DewDLConfigs.update_key_path(Path(config_value))
