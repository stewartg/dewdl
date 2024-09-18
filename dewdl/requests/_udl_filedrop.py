from collections import UserString

from dewdl.enums import UDLEnvironment, UDLFileDropType


class UDLFileDrop(UserString):
    def __init__(self, data_endpoint: UDLFileDropType, udl_environment: UDLEnvironment) -> None:
        self._base_url = udl_environment.value
        self._end_point = data_endpoint.value
        super().__init__(self._build_base_url())

    def _build_base_url(self) -> str:
        return "/".join([self._base_url, self._end_point])

    def to_string(self) -> str:
        return self.data
