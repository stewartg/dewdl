import sys

from dewdl import DewDLConfigs
from dewdl._cli._config_interface import delete, set_config


def run():
    if sys.argv[1] == "config":
        if sys.argv[2] == "show":
            if len(sys.argv) == 3:
                sys.argv.append("")
            DewDLConfigs.debug(sys.argv[3])
        elif sys.argv[2] == "delete":
            delete(sys.argv[3])
        else:
            set_config(sys.argv[2], sys.argv[3])
