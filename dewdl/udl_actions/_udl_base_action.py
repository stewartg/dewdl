from collections import UserString


class UDLBaseAction(UserString):
    def __init__(self, data_endpoint: str, udl_environment: str) -> None:
        self._base_url = udl_environment
        self._end_point = data_endpoint
        super().__init__(self._build_base_url())

    def _build_base_url(self) -> str:
        return "/".join([self._base_url, self._end_point])

    def to_string(self) -> str:
        return self.data
