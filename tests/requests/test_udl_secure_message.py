from dewdl.enums import UDLEnvironment, UDLSecureMessageTopic
from dewdl.requests import UDLSecureMessage


def test_get_topics():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    import json

    json.dump(sms.topics, open("topics.json", "w"))
    assert sms.topics[0]["topic"] == "geostatus"


def test_get_latest_offset():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    assert sms.get_latest_offset(UDLSecureMessageTopic.ELSET)


def test_describe_topic():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    assert sms.describe_topic(UDLSecureMessageTopic.ELSET).topic == UDLSecureMessageTopic.ELSET.value


def test_get_messages():
    sms = UDLSecureMessage(environment=UDLEnvironment.TEST)
    last_offset = sms.get_latest_offset(UDLSecureMessageTopic.ELSET)
    assert sms.get_messages(UDLSecureMessageTopic.ELSET, last_offset) == []
