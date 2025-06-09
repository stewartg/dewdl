import io
import json
import re
import zipfile
from pathlib import Path

import httpx
import pytest
from mockito import mock, verifyNoUnwantedInteractions, when

from dewdl import DewDLConfigs
from dewdl.enums import UDLEnvironment, UDLFileDropType, UDLQueryType
from dewdl.requests import UDLRequest
from dewdl.requests.udl_request_payload import UDLRequestPayload
from dewdl.udl_actions import UDLFileDrop, UDLQuery


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
def valid_udl_elset_zip():
    data = {
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

    # Convert the dictionary to JSON string
    json_data = json.dumps(data).encode("utf-8")

    # Create a zip file in memory
    with io.BytesIO() as bytes_io:
        with zipfile.ZipFile(bytes_io, "w") as zip_file:
            zip_file.writestr("data.json", json_data)

        # Get the byte data of the zip file
        return bytes_io.getvalue()


@pytest.fixture
def test_certs():
    f_path = Path(__file__)
    test_certs_dir = Path(str(f_path.parents[1]), "test_data/certs")
    return {"crt": f"{test_certs_dir}/test_cert.pem", "key": f"{test_certs_dir}/test_key.pem"}


@pytest.mark.usefixtures("_unstub")
def test_get_from_udl_with_cert(test_certs):
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST).with_uuid("c60092be-9220-4f22-b0e4-5e5731341e7a")
    payload = UDLRequestPayload(endpoint=udl_endpoint, crt=test_certs["crt"], key=test_certs["key"])
    # Mock the _make_request method of UDLRequest
    mock_response = mock()
    # Set the status_code attribute on the mock response object
    mock_response.status_code = 200
    # Mock httpx.Client and ensure the certificate paths are used
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client(cert=(str(payload.crt), str(payload.key)), verify=True).thenReturn(client_mock)
    when(client_mock).get(udl_endpoint.to_string(), timeout=30).thenReturn(mock_response)
    response = UDLRequest._make_request(payload=payload)
    assert response.status_code == 200
    verifyNoUnwantedInteractions()


@pytest.mark.usefixtures("_unstub")
def test_get_from_udl_with_b64():
    # Mock the get_b64_key method to return a mocked value
    mock_b64_key = "Basic mocked_base64_key"
    when(DewDLConfigs).get_b64_key().thenReturn(mock_b64_key)
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST).with_uuid("0a040967-b9c1-4609-a62f-090e8970a235")
    payload = UDLRequestPayload(endpoint=udl_endpoint, b64_key=DewDLConfigs.get_b64_key())
    # Mock the _make_request method of UDLRequest
    mock_response = mock()
    # Set the status_code attribute on the mock response object
    mock_response.status_code = 200
    # Mock httpx.Client
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client().thenReturn(client_mock)
    when(client_mock).get(udl_endpoint.to_string(), timeout=30).thenReturn(mock_response)
    response = UDLRequest._make_request(payload=payload)
    assert response.status_code == 200
    verifyNoUnwantedInteractions()


@pytest.mark.usefixtures("_unstub")
def test_post_to_udl_with_cert(valid_udl_elset, test_certs):
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST)
    payload = UDLRequestPayload(
        endpoint=udl_endpoint, method="POST", post_body=valid_udl_elset, crt=test_certs["crt"], key=test_certs["key"]
    )
    # Mock response object
    mock_response = mock()
    uuid = "c60092be-9220-4f22-b0e4-5e5731341e7a"
    mock_response.status_code = 201
    mock_response.headers = {"location": f"{UDLEnvironment.TEST}/{uuid}"}
    # Mock httpx.Client and ensure the certificate paths are used
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client(cert=(str(payload.crt), str(payload.key)), verify=True).thenReturn(client_mock)
    when(client_mock).post(udl_endpoint.to_string(), headers=any, data=any, timeout=30).thenReturn(mock_response)
    uuid = UDLRequest._make_request(payload=payload)
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)
    verifyNoUnwantedInteractions()


@pytest.mark.usefixtures("_unstub")
def test_post_to_udl_with_b64(valid_udl_elset):
    # Mock the get_b64_key method to return a mocked value
    mock_b64_key = "Basic mocked_base64_key"
    when(DewDLConfigs).get_b64_key().thenReturn(mock_b64_key)
    udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST)
    payload = UDLRequestPayload(
        endpoint=udl_endpoint, method="POST", post_body=valid_udl_elset, b64_key=DewDLConfigs.get_b64_key()
    )
    # Mock response object
    mock_response = mock()
    uuid = "c60092be-9220-4f22-b0e4-5e5731341e7a"
    mock_response.status_code = 201
    mock_response.headers = {"location": f"{UDLEnvironment.TEST}/{uuid}"}
    # Mock httpx.Client and make it compatible with the context manager protocol
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client().thenReturn(client_mock)

    # Configure the post method on client_mock to return mock_response
    when(client_mock).post(udl_endpoint, headers=any, data=any, timeout=30).thenReturn(mock_response)

    uuid = UDLRequest._make_request(payload=payload)
    uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
    assert re.match(uuid_regex, uuid)
    verifyNoUnwantedInteractions()


@pytest.mark.usefixtures("_unstub")
def test_filedrop_with_cert(valid_udl_elset, test_certs):
    # Mock the Path class to avoid using hardcoded file paths
    udl_endpoint = UDLFileDrop(UDLFileDropType.ELSET, UDLEnvironment.TEST)
    payload = UDLRequestPayload(
        endpoint=udl_endpoint,
        method="POST",
        post_body=valid_udl_elset,
        crt=test_certs["crt"],
        key=test_certs["key"],
        is_filedrop=True,
    )
    # Mock response object
    mock_response = mock()
    mock_response.status_code = 202
    mock_response.text = "Accepted"
    # Mock httpx.Client and ensure the certificate paths are used
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client(cert=(str(payload.crt), str(payload.key)), verify=True).thenReturn(client_mock)
    when(client_mock).post(udl_endpoint.to_string(), headers=any, data=any, timeout=30).thenReturn(mock_response)
    response_txt = UDLRequest._make_request(payload=payload)
    assert response_txt == "Accepted"
    verifyNoUnwantedInteractions()


@pytest.mark.usefixtures("_unstub")
def test_post_zip_to_udl_with_cert(valid_udl_elset_zip, test_certs):
    udl_endpoint = UDLQuery(UDLQueryType.SKY_IMAGERY, UDLEnvironment.TEST)
    payload = UDLRequestPayload(
        endpoint=udl_endpoint,
        method="POST",
        is_filedrop=True,
        zip_data=valid_udl_elset_zip,
        crt=test_certs["crt"],
        key=test_certs["key"],
    )
    # Mock response object
    mock_response = mock()
    mock_response.status_code = 202
    mock_response.text = "Accepted"
    # Mock httpx.Client and ensure the certificate paths are used
    client_mock = mock(httpx.Client)
    when(client_mock).__enter__().thenReturn(client_mock)
    when(client_mock).__exit__(...).thenReturn(None)
    when(httpx).Client(cert=(str(payload.crt), str(payload.key)), verify=True).thenReturn(client_mock)
    when(client_mock).post(udl_endpoint.to_string(), headers=any, data=any, timeout=30).thenReturn(mock_response)
    response_txt = UDLRequest._make_request(payload=payload)
    assert response_txt == "Accepted"
    verifyNoUnwantedInteractions()


# def test_post_with_cert_config(valid_udl_elset):
#     udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD)
#     uuid = UDLRequest.post(udl_endpoint, valid_udl_elset)
#     uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
#     assert re.match(uuid_regex, uuid)


# def test_post_without_cert_config(valid_udl_elset):
#     when(DewDLConfigs).get_crt_path().thenReturn(None)
#     when(DewDLConfigs).get_key_path().thenReturn(None)
#     udl_endpoint = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.TEST)
#     uuid = UDLRequest.post(udl_endpoint, valid_udl_elset)
#     uuid_regex = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$"
#     assert re.match(uuid_regex, uuid)


# def test_filedrop_with_cert_config(valid_udl_elset):
#     udl_endpoint = UDLFileDrop(UDLFileDropType.ELSET, UDLEnvironment.PROD)
#     UDLRequest.filedrop(udl_endpoint, [valid_udl_elset])


# def test_filedrop_without_cert_config(valid_udl_elset):
#     when(DewDLConfigs).get_crt_path().thenReturn(None)
#     when(DewDLConfigs).get_key_path().thenReturn(None)
#     udl_endpoint = UDLFileDrop(UDLFileDropType.ELSET, UDLEnvironment.PROD)
#     UDLRequest.filedrop(udl_endpoint, [valid_udl_elset])
