from __future__ import annotations

import time
from datetime import datetime

import httpx

from dewdl import DewDLConfigs
from dewdl.enums import UDLSecureMessageType
from dewdl.enums._udl_base_data_type import UDLBaseDataType
from dewdl.enums._udl_date_fields import UDLDateFields
from dewdl.models import TopicDescription
from dewdl.models._sms_response import SMSResponse
from dewdl.udl_actions._udl_sms_base_action import UDLSMSBaseAction


class UDLSecureMessage(UDLSMSBaseAction):
    MESSAGE_RATE_LIMIT = 3  # 3 requests per second
    MINIMUM_MESSAGE_FREQUENCY = 1 / MESSAGE_RATE_LIMIT

    def __init__(self, udl_data_type: UDLBaseDataType, **query_params) -> None:
        super().__init__(udl_data_type.value, **query_params)
        self.base_data_type = udl_data_type
        self.time_key = UDLDateFields.get(self.base_data_type)
        self.dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        self._time = ""
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
        self.last_request_time = 0.0

    @property
    def topics(self) -> list[dict]:
        url = "/".join([self._base_url, UDLSecureMessageType.TOPICS.value])
        return self.client.get(url).json()

    def get_latest_offset(self) -> int:
        url = "/".join([self._base_url, UDLSecureMessageType.LATEST_OFFSET.value, self._sms_topic])
        return int(self.client.get(url).text)

    def describe_topic(self) -> TopicDescription:
        url = "/".join([self._base_url, UDLSecureMessageType.DESCRIBE_TOPIC.value, self._sms_topic])
        return TopicDescription.model_validate(self.client.get(url).json())

    def get_messages(self, offset: int) -> SMSResponse:
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.MINIMUM_MESSAGE_FREQUENCY:
            time.sleep(self.MINIMUM_MESSAGE_FREQUENCY - time_since_last_request)

        self.update_offset(offset)
        url = self._regenerate().to_string()

        response = self.client.get(url)
        # Raise standard HTTP errors (404, 500, etc.)
        response.raise_for_status()

        # Only parse if content exists; otherwise default to empty list
        json_data = response.json() if response.content else []

        sms_dict = {
            "data": json_data,
            "next_offset": response.headers.get("KAFKA_NEXT_OFFSET", offset),
        }

        return SMSResponse.model_validate(sms_dict)

    def after(self, epoch: datetime) -> UDLSecureMessage:
        epoch_str = epoch.strftime(self.dt_format)
        self._time = f"{self.time_key}=%3E{epoch_str}"
        return self._regenerate()

    def before(self, epoch: datetime) -> UDLSecureMessage:
        epoch_str = epoch.strftime(self.dt_format)
        self._time = f"{self.time_key}=%3C{epoch_str}"
        return self._regenerate()

    def between(self, start: datetime, end: datetime) -> UDLSecureMessage:
        start_str = start.strftime(self.dt_format)
        end_str = end.strftime(self.dt_format)
        self._time = f"{self.time_key}={start_str}..{end_str}"
        return self._regenerate()

    def get_messages_and_sm_header(self, topic: UDLBaseDataType, offset: int) -> tuple:
        url = "/".join([self._base_url, UDLSecureMessageType.MESSAGES.value, topic.value, str(offset)])
        response_object = self.session.get(url)
        response_object.raise_for_status()
        sm_header = response_object.headers
        messages = response_object.json()
        return messages, sm_header

    def _regenerate(self) -> UDLSecureMessage:
        base_str = self._build_base_url()
        valid_queries = [val for val in [self._time] if val]
        query_str = "&".join(valid_queries)
        if len(valid_queries) == 1:
            query_str = "&" + query_str
        full_str = "".join([base_str, query_str]) if query_str else base_str
        self.data = full_str
        return self
