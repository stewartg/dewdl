from collections import UserString

from dewdl._dewdl_configs import DewDLConfigs
from dewdl.enums._udl_environment import UDLEnvironment
from dewdl.enums._udl_secure_message_type import UDLSecureMessageType


class UDLSMSBaseAction(UserString):
    def __init__(self, sms_topic: str, **query_params) -> None:
        udl_env = DewDLConfigs.get_udl_env()
        if udl_env not in ["test", "prod"]:
            raise ValueError("Invalid UDL environment specified")
        self._base_url = UDLEnvironment.TEST.value if udl_env == "test" else UDLEnvironment.PROD.value
        self._sms_topic = sms_topic
        self._query_params = query_params
        # Initialize offset as a placeholder
        self.offset = "${OFFSET}"
        super().__init__(self._build_base_url())

    def _build_base_url(self) -> str:
        url = "/".join([self._base_url, UDLSecureMessageType.MESSAGES.value, self._sms_topic, self.offset])
        # Remove query parameters with None values.
        query_string = "&".join(f"{key}={value}" for key, value in self._query_params.items() if value is not None)
        if query_string:
            url += f"?{query_string}"
        return url

    def update_offset(self, new_offset: int) -> None:
        self.offset = str(new_offset)
        self.data = self._build_base_url()

    def to_string(self) -> str:
        return self.data
