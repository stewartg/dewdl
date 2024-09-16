import sys

from dewdl import DewDLConfigs
from dewdl._cli._config_interface import set_config


def run():
    if sys.argv[1] == "config":
        if sys.argv[2] == "show":
            DewDLConfigs.debug()
        else:
            set_config(sys.argv[2], sys.argv[3])
