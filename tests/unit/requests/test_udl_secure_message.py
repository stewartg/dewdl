from datetime import datetime

import pytest

from dewdl import DewDLConfigs
from dewdl.enums import UDLBaseDataType, UDLEnvironment
from dewdl.udl_actions._udl_secure_message import UDLSecureMessage


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_topics():
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.EO_OBSERVATION)
    topics = sms.topics
    assert topics is not None, "UDLSecureMessage topics should not be None"
    assert any(elem.get("topic") == "geostatus" for elem in topics), "There should be a topic with 'geostatus'"


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_latest_offset():
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.ELSET)
    assert sms.get_latest_offset()


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_describe_topic():
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.ELSET)
    assert sms.describe_topic().topic == UDLBaseDataType.ELSET.value


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_messages_no_params_no_date_query():
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.ELSET)
    last_offset = sms.get_latest_offset()
    response = sms.get_messages(last_offset)
    assert response.data == []


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_messages_with_params_no_date_query():
    params = {"dataMode": "real"}
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.ELSET, **params)
    last_offset = sms.get_latest_offset()
    response = sms.get_messages(last_offset)
    assert sms.to_string() == (
        f"{UDLEnvironment.TEST.value}/sm/getMessages/" f"{UDLBaseDataType.ELSET.value}/{last_offset}" "?dataMode=real"
    )
    assert response.data == []


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_messages_with_params_and_date_query():
    params = {"dataMode": "real"}
    epoch = datetime(2015, 9, 16)
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.ELSET, **params).after(epoch)
    last_offset = sms.get_latest_offset()
    response = sms.get_messages(last_offset)
    assert sms.to_string() == (
        f"{UDLEnvironment.TEST.value}/sm/getMessages/"
        f"{UDLBaseDataType.ELSET.value}/{last_offset}"
        "?dataMode=real&epoch=%3E2015-09-16T00:00:00.000000Z"
    )
    assert response.data == []


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_messages_streaming():
    sms = UDLSecureMessage(udl_data_type=UDLBaseDataType.EO_OBSERVATION)
    last_offset = sms.get_latest_offset() - 1000
    for _ in range(3):  # Example loop to
        message_resp = sms.get_messages(last_offset)
        assert message_resp.data is not None
        last_offset = message_resp.next_offset
