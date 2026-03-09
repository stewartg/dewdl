from enum import Enum

from dewdl.enums._udl_base_data_type import UDLBaseDataType


class UDLDateFields(Enum):
    DIFF_OF_ARRIVAL = (UDLBaseDataType.DIFF_OF_ARRIVAL, None)
    ELSET = (UDLBaseDataType.ELSET, None)
    EO_OBSERVATION = (UDLBaseDataType.EO_OBSERVATION, "obTime")
    NOTIFICATION = (UDLBaseDataType.NOTIFICATION, "createdAt")
    ONORBIT = (UDLBaseDataType.ONORBIT, None)
    SKY_IMAGERY = (UDLBaseDataType.SKY_IMAGERY, None)
    SOI_OBSERVATION = (UDLBaseDataType.SOI_OBSERVATION, "startTime")
    STATE_VECTOR = (UDLBaseDataType.STATE_VECTOR, None)

    def __init__(self, base_data_type, date_field):
        self.base_data_type = base_data_type
        self.date_field = date_field

    @classmethod
    def get(cls, base_data_type):
        return next((field.date_field or "epoch" for field in cls if field.base_data_type == base_data_type), "epoch")


if __name__ == "__main__":
    test_cases = [
        UDLBaseDataType.DIFF_OF_ARRIVAL,
        UDLBaseDataType.ELSET,
        UDLBaseDataType.EO_OBSERVATION,
        UDLBaseDataType.NOTIFICATION,
        UDLBaseDataType.ONORBIT,
        UDLBaseDataType.SKY_IMAGERY,
        UDLBaseDataType.SOI_OBSERVATION,
        UDLBaseDataType.STATE_VECTOR,
    ]

    for base_data_type in test_cases:
        date_field = UDLDateFields.get(base_data_type)
        print(f"Base Data Type: {base_data_type.name}, Date Field: {date_field}")
