import logging
from pythonjsonlogger import jsonlogger
from dewdl._dewdl_configs import DewDLConfigs

DEWDL_LOG = logging.getLogger(__name__)
DEWDL_LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(filename)s %(module)s %(funcName)s %(lineno)s %(message)s",
    rename_fields={
        "asctime": "time",
        "levelname": "level",
        "filename": "file",
        "funcName": "function",
        "lineno": "line",
    },
)
handler.setFormatter(formatter)
DEWDL_LOG.addHandler(handler)

DewDLConfigs.load_config_file()
