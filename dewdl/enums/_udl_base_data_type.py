from enum import Enum


class UDLBaseDataType(Enum):
    DIFF_OF_ARRIVAL = "diffofarrival"
    ELSET = "elset"
    EO_OBSERVATION = "eoobservation"
    MANEUVER = "maneuver"
    NOTIFICATION = "notification"
    ONORBIT = "onorbit"
    SKY_IMAGERY = "skyimagery"
    SOI_OBSERVATION = "soiobservationset"
    STATE_VECTOR = "statevector"
