import pytest
from mockito import mock  # type: ignore

from dewdl.exceptions import UDLRequestError


@pytest.fixture
def mock_401_response():
    return mock({"status_code": 401, "text": "Unauthorized"})


@pytest.fixture
def mock_unknown_with_msg_response():
    return mock({"status_code": -1, "text": '{"message": "Unknown error"}'})


@pytest.fixture
def mock_unknown_no_msg_response():
    return mock({"status_code": -1, "text": "{}"})


def test_invalid_credentials(mock_401_response):

    with pytest.raises(UDLRequestError) as error_message:
        raise UDLRequestError(mock_401_response)

    assert str(error_message.value) == "401 Unauthorized - Verify credentials and try again."


def test_unknown_with_msg(mock_unknown_with_msg_response):

    with pytest.raises(UDLRequestError) as error_message:
        raise UDLRequestError(mock_unknown_with_msg_response)

    assert str(error_message.value) == "-1 - Unknown error"


def test_unknown_without_msg(mock_unknown_no_msg_response):

    with pytest.raises(UDLRequestError) as error_message:
        raise UDLRequestError(mock_unknown_no_msg_response)

    assert str(error_message.value) == "-1 - Unexpected response"
