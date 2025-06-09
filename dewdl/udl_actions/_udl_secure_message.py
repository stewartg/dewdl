from __future__ import annotations

import httpx

from dewdl import DewDLConfigs
from dewdl.enums import UDLEnvironment, UDLSecureMessageTopic, UDLSecureMessageType
from dewdl.models import TopicDescription


class UDLSecureMessage:
    def __init__(self, environment: UDLEnvironment) -> None:
        timeout = 30
        cert = None
        if DewDLConfigs.has_cert() and DewDLConfigs.has_key():
            crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
            cert = (crt.as_posix(), key.as_posix())
        auth = None
        if DewDLConfigs.has_user() and DewDLConfigs.has_password():
            user, password = DewDLConfigs.get_user(), DewDLConfigs.get_password()
            auth = (user, password)
        if cert:
            self.client = httpx.Client(cert=cert, verify=True, timeout=timeout)
        elif auth:
            self.client = httpx.Client(auth=auth, timeout=timeout)
        else:
            self.client = httpx.Client(timeout=timeout)
        self._base_url = environment.value

    @property
    def topics(self) -> list[dict]:
        url = "/".join([self._base_url, UDLSecureMessageType.TOPICS.value])
        return self.client.get(url).json()

    def get_latest_offset(self, topic: UDLSecureMessageTopic) -> int:
        url = "/".join([self._base_url, UDLSecureMessageType.LATEST_OFFSET.value, topic.value])
        return int(self.client.get(url).text)

    def describe_topic(self, topic: UDLSecureMessageTopic) -> TopicDescription:
        url = "/".join([self._base_url, UDLSecureMessageType.DESCRIBE_TOPIC.value, topic.value])
        return TopicDescription.model_validate(self.client.get(url).json())

    def get_messages(self, topic: UDLSecureMessageTopic, offset: int) -> list[dict]:
        url = "/".join([self._base_url, UDLSecureMessageType.MESSAGES.value, topic.value, str(offset)])
        return self.client.get(url).json()
