from dewdl.enums import UDLQueryType
from dewdl.udl_actions import UDLBaseAction


class UDLGetFile(UDLBaseAction):
    def __init__(self, data_endpoint: UDLQueryType, id: str) -> None:
        super().__init__(f"{data_endpoint.value}/getFile/{id}")
