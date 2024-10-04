import re
from pathlib import Path

import pytest
from mockito import unstub, when  # type: ignore

from dewdl import DewDLConfigs
from dewdl.enums import UDLEnvironment, UDLFileDropType, UDLQueryType
from dewdl.models import Elset
from dewdl.requests import UDLFileDrop, UDLQuery, UDLRequest
from dewdl.requests._udl_request import (
    _get_from_udl_with_b64,
    _get_from_udl_with_cert,
    _post_to_udl_with_b64,
    _post_to_udl_with_cert,
)


@pytest.fixture
def valid_udl_elset():
    return {
        "classificationMarking": "U",
        "satNo": 12,
        "epoch": "2018-01-01T16:00:00.123456Z",
        "meanMotion": 1.1,
        "eccentricity": 0.333,
        "inclination": 45.1,
        "raan": 1.1,
        "argOfPerigee": 1.1,
        "meanAnomaly": 179.1,
        "origin": "DnD",
        "source": "SSDP",
        "dataMode": "TEST",
    }


@pytest.fixture
def _unstub_dewdl_configs(autouse=True):
    unstub()
    yield
    unstub()


def test_get_from_udl_with_cert():

    crt, key = Path("certs/dnd-ssdp-udl.crt"), Path("certs/dnd-ssdp-udl.key")
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD).with_uuid("c60092be-9220-4f22-b0e4-5e5731341e7a")
    response = _get_from_udl_with_cert(udl_endpoint, crt, key)

    assert response.status_code == 200


def test_get_from_udl_with_b64():
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST).with_uuid("0a040967-b9c1-4609-a62f-090e8970a235")
    response = _get_from_udl_with_b64(udl_endpoint, DewDLConfigs.get_b64_key())
    assert response.status_code == 200


def test_post_to_udl_with_cert(valid_udl_elset):

    crt, key = Path("certs/dnd-ssdp-udl.crt"), Path("certs/dnd-ssdp-udl.key")
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD)
    uuid = _post_to_udl_with_cert(udl_endpoint, valid_udl_elset, crt, key)
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)


def test_post_to_udl_with_b64(valid_udl_elset):
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST)
    uuid = _post_to_udl_with_b64(udl_endpoint, valid_udl_elset, DewDLConfigs.get_b64_key())
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)


def test_get_with_cert_config():
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD).with_uuid("c60092be-9220-4f22-b0e4-5e5731341e7a")
    response = UDLRequest.get(udl_endpoint)
    elset = Elset.model_validate(response.json())
    assert response.status_code == 200
    assert elset.idElset == "c60092be-9220-4f22-b0e4-5e5731341e7a"


def test_get_without_cert_config():
    when(DewDLConfigs).get_crt_path().thenReturn(None)
    when(DewDLConfigs).get_key_path().thenReturn(None)
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST).with_uuid("0a040967-b9c1-4609-a62f-090e8970a235")
    response = UDLRequest.get(udl_endpoint)
    elset = Elset.model_validate(response.json())
    assert response.status_code == 200
    assert elset.idElset == "0a040967-b9c1-4609-a62f-090e8970a235"


def test_post_with_cert_config(valid_udl_elset):
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD)
    uuid = UDLRequest.post(udl_endpoint, valid_udl_elset)
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)


def test_post_without_cert_config(valid_udl_elset):
    when(DewDLConfigs).get_crt_path().thenReturn(None)
    when(DewDLConfigs).get_key_path().thenReturn(None)
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST)
    uuid = UDLRequest.post(udl_endpoint, valid_udl_elset)
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)


def test_filedrop_with_cert_config(valid_udl_elset):
    udl_endpoint = UDLFileDrop(UDLFileDropType.ELSET, UDLEnvironment.PROD)
    UDLRequest.filedrop(udl_endpoint, [valid_udl_elset])


def test_filedrop_without_cert_config(valid_udl_elset):
    when(DewDLConfigs).get_crt_path().thenReturn(None)
    when(DewDLConfigs).get_key_path().thenReturn(None)
    udl_endpoint = UDLFileDrop(UDLFileDropType.ELSET, UDLEnvironment.PROD)
    UDLRequest.filedrop(udl_endpoint, [valid_udl_elset])
