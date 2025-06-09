import pytest

from dewdl import DewDLConfigs
from dewdl.enums import UDLEnvironment, UDLSecureMessageTopic
from dewdl.udl_actions._udl_secure_message import UDLSecureMessage


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_topics():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    topics = sms.topics
    assert topics is not None, "UDLSecureMesage topics should not be None"
    assert any(elem.get("topic") == "geostatus" for elem in topics), "There should be a topic with 'geostatus'"


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_latest_offset():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    assert sms.get_latest_offset(UDLSecureMessageTopic.ELSET)


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_describe_topic():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    assert sms.describe_topic(UDLSecureMessageTopic.ELSET).topic == UDLSecureMessageTopic.ELSET.value


@pytest.mark.skipif(
    not (DewDLConfigs.has_user() and DewDLConfigs.has_password()), reason="DewDLConfigs user and password are not set"
)
def test_get_messages():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    last_offset = sms.get_latest_offset(UDLSecureMessageTopic.ELSET)
    assert sms.get_messages(UDLSecureMessageTopic.ELSET, last_offset) == []
