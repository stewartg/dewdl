from enum import Enum


class UDLQueryType(Enum):
    EO_OBSERVATION = "udl/eoobservation"
    ELSET = "udl/elset"
    NOTIFICATION = "udl/notification"
