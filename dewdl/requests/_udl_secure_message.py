from __future__ import annotations

from requests import Session  # type: ignore

from dewdl import DewDLConfigs
from dewdl.enums import UDLEnvironment, UDLSecureMessageTopic, UDLSecureMessageType
from dewdl.models import TopicDescription


class UDLSecureMessage:
    def __init__(self, environment: UDLEnvironment) -> None:
        self.session = Session()
        crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
        user, password = None, None
        if crt is not None and key is not None:
            self.session.cert = (crt.as_posix(), key.as_posix())
        else:
            user, password = DewDLConfigs.get_user(), DewDLConfigs.get_password()

        if user is not None and password is not None:
            self.session.auth = (user, password)
        self._base_url = environment.value

    @property
    def topics(self) -> list[dict]:
        url = "/".join([self._base_url, UDLSecureMessageType.TOPICS.value])
        return self.session.get(url).json()

    def get_latest_offset(self, topic: UDLSecureMessageTopic) -> int:
        url = "/".join([self._base_url, UDLSecureMessageType.LATEST_OFFSET.value, topic.value])
        return int(self.session.get(url).text)

    def describe_topic(self, topic: UDLSecureMessageTopic) -> TopicDescription:
        url = "/".join([self._base_url, UDLSecureMessageType.DESCRIBE_TOPIC.value, topic.value])
        return TopicDescription.model_validate(self.session.get(url).json())

    def get_messages(self, topic: UDLSecureMessageTopic, offset: int) -> list[dict]:
        url = "/".join([self._base_url, UDLSecureMessageType.MESSAGES.value, topic.value, str(offset)])
        return self.session.get(url).json()
