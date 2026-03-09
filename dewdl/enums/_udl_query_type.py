from enum import Enum

from dewdl.enums._udl_base_data_type import UDLBaseDataType


class UDLQueryType(Enum):
    DIFF_OF_ARRIVAL = UDLBaseDataType.DIFF_OF_ARRIVAL
    ELSET = UDLBaseDataType.ELSET
    EO_OBSERVATION = UDLBaseDataType.EO_OBSERVATION
    NOTIFICATION = UDLBaseDataType.NOTIFICATION
    ONORBIT = UDLBaseDataType.ONORBIT
    SKY_IMAGERY = UDLBaseDataType.SKY_IMAGERY
    SOI_OBSERVATION = UDLBaseDataType.SOI_OBSERVATION
    STATE_VECTOR = UDLBaseDataType.STATE_VECTOR

    def __init__(self, base_data_type):
        self.base_data_type = base_data_type

    @property
    def value(self):
        return f"udl/{self.base_data_type.value}"
