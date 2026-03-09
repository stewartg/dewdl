from dewdl.enums import UDLFileDropType
from dewdl.udl_actions._udl_base_action import UDLBaseAction


class UDLFileDrop(UDLBaseAction):
    def __init__(self, data_endpoint: UDLFileDropType) -> None:
        super().__init__(data_endpoint.value)
