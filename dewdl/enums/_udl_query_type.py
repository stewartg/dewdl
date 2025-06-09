from enum import Enum


class UDLQueryType(Enum):
    EO_OBSERVATION = "udl/eoobservation"
    ELSET = "udl/elset"
    NOTIFICATION = "udl/notification"
    ONORBIT = "udl/onorbit"
    SKY_IMAGERY = "udl/skyimagery"
    STATE_VECTOR = "udl/statevector"
