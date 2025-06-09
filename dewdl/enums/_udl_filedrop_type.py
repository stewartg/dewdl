from enum import Enum


class UDLFileDropType(Enum):
    ELSET = "filedrop/udl-elset"
    EO_OBS = "filedrop/udl-eo"
    SKY_IMAGERY = "filedrop/udl-skyimagery"
    STATE_VECTOR = "filedrop/udl-sv"
