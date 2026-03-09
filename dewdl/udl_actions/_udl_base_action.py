from collections import UserString

from dewdl._dewdl_configs import DewDLConfigs
from dewdl.enums._udl_environment import UDLEnvironment


class UDLBaseAction(UserString):
    def __init__(self, data_endpoint: str) -> None:
        udl_env = DewDLConfigs.get_udl_env()
        if udl_env not in ["test", "prod"]:
            raise ValueError("Invalid UDL environment specified")

        self._base_url = UDLEnvironment.TEST.value if udl_env == "test" else UDLEnvironment.PROD.value
        self._end_point = data_endpoint
        super().__init__(self._build_base_url())

    def _build_base_url(self) -> str:
        return "/".join([self._base_url, self._end_point])

    def to_string(self) -> str:
        return self.data
