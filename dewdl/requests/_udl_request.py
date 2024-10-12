import json
from pathlib import Path

import requests  # type: ignore
from requests.models import Response  # type: ignore

from dewdl import DEWDL_LOG, DewDLConfigs
from dewdl.enums import UDLRequestSuccessCode
from dewdl.exceptions import UDLRequestError
from dewdl.requests._udl_filedrop import UDLFileDrop
from dewdl.requests._udl_query import UDLQuery


class UDLRequest:
    @staticmethod
    def format_booleans(input_str: str) -> str:
        """Converts the string 'True' to 'true' and 'False' to 'False'

        :param input_str: The string to convert
        """
        return input_str.replace("True", "true").replace("False", "false")

    @staticmethod
    def post(endpoint: UDLQuery, post_body: dict) -> str:
        crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
        if crt is not None and key is not None:
            uuid_str = _post_to_udl_with_cert(endpoint, post_body, crt, key)
        else:
            uuid_str = _post_to_udl_with_b64(endpoint, post_body, DewDLConfigs.get_b64_key())
        return uuid_str

    @staticmethod
    def filedrop(endpoint: UDLFileDrop, post_body: list[dict]) -> None:
        crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
        if crt is not None and key is not None:
            _filedrop_to_udl_with_cert(endpoint, post_body, crt, key)
        else:
            _filedrop_to_udl_with_b64(endpoint, post_body, DewDLConfigs.get_b64_key())

    @staticmethod
    def get(endpoint: UDLQuery) -> Response:
        crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
        if crt is not None and key is not None:
            udl_response = _get_from_udl_with_cert(endpoint, crt, key)
        else:
            udl_response = _get_from_udl_with_b64(endpoint, DewDLConfigs.get_b64_key())
        return udl_response


def _filedrop_to_udl_with_b64(udl_endpoint: UDLFileDrop, post_body: list[dict], b64_key: str) -> None:
    """Performs a POST request of bulk data to the UDL server using a base64 encoded key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str
    :param json_str: JSON-formatted string to send to the UDL
    :type json_str: str

    :raises: UDLRequestError: If the response code is not 202
    """
    # create the headers for the post request
    udl_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": b64_key,
    }

    # convert the post body to a string and correct boolean case
    json_str = json.dumps(post_body)
    body_str = UDLRequest.format_booleans(json_str)

    # send the post request
    DEWDL_LOG.info(f"Publishing {len(post_body)} records to {udl_endpoint.to_string()} using base64 key")
    response = requests.post(udl_endpoint.to_string(), data=body_str, verify=True, headers=udl_headers)

    # check for successful post
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.FILEDROP:
        raise UDLRequestError(response)


def _filedrop_to_udl_with_cert(
    udl_endpoint: UDLFileDrop, post_body: list[dict], cert_path: Path, key_path: Path
) -> str:
    """Performs a POST request of bulk data to the UDL server using a certificate and key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str
    :param json_str: JSON-formatted string to send to the UDL
    :type json_str: str

    :raises: UDLRequestError: If the response code is not 202
    """
    # create the headers for the post request
    udl_headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    # convert the post body to a string and correct boolean case
    json_str = json.dumps(post_body)
    body_str = UDLRequest.format_booleans(json_str)

    # send the post request
    DEWDL_LOG.info(f"Publishing {len(post_body)} records to {udl_endpoint.to_string()} crt={cert_path} key={key_path}")
    response = requests.post(
        udl_endpoint.to_string(),
        data=body_str,
        verify=True,
        headers=udl_headers,
        cert=(cert_path.as_posix(), key_path.as_posix()),
    )

    # check for successful post
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.FILEDROP:
        raise UDLRequestError(response)

    return response.text


def _post_to_udl_with_b64(udl_endpoint: UDLQuery, post_body: dict, b64_key: str) -> str:
    """Performs a POST request to the UDL server using a base64 encoded key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str
    :param json_str: JSON string to send to the UDL server
    :type json_str: str

    :raises UDLRequestError: If the response code is not 201
    :raises KeyError: If no UUID is returned from the UDL

    :return: The UUID generated by the UDL after posting
    :rtype: str
    """

    # create the headers for the post request
    udl_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": b64_key,
    }

    # convert the post body to a string and correct boolean case
    json_str = json.dumps(post_body)
    body_str = UDLRequest.format_booleans(json_str)

    # send the post request
    DEWDL_LOG.info(f"Publishing to {udl_endpoint.to_string()} using base64 key")
    response = requests.post(udl_endpoint.to_string(), data=body_str, verify=False, headers=udl_headers)

    # check for successful post
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.POST:
        raise UDLRequestError(response)

    # check for location of newly posted data
    url = response.headers.get("location")
    if url is None:
        raise KeyError("No UUID returned from UDL")

    # parse the UUID from the URL
    posted_uuid = url.split("/")[-1]

    return posted_uuid


def _post_to_udl_with_cert(udl_endpoint: UDLQuery, post_body: dict, cert_path: Path, key_path: Path) -> str:
    """Performs a POST request to the UDL server using a certificate and key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str
    :param json_str: JSON string to send to the UDL server
    :type json_str: str

    :raises UDLRequestError: If the response code is not 201
    :raises KeyError: If no UUID is returned from the UDL

    :return: The UUID generated by the UDL after posting
    :rtype: str
    """

    # create the headers for the post request
    udl_headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    # convert the post body to a string and correct boolean case
    json_str = json.dumps(post_body)
    body_str = UDLRequest.format_booleans(json_str)

    # send the post request
    DEWDL_LOG.info(f"Publishing to {udl_endpoint.to_string()} crt={cert_path} key={key_path}")
    response = requests.post(
        udl_endpoint.to_string(),
        data=body_str,
        verify=True,
        headers=udl_headers,
        cert=(cert_path.as_posix(), key_path.as_posix()),
    )

    # check for successful post
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.POST:
        raise UDLRequestError(response)

    # check for location of newly posted data
    url = response.headers.get("location")
    if url is None:
        raise KeyError("No UUID returned from UDL")

    # parse the UUID from the URL
    posted_uuid = url.split("/")[-1]

    return posted_uuid


def _get_from_udl_with_b64(udl_endpoint: UDLQuery, b64_key: str) -> Response:
    """Performs a GET request to the UDL server using a base64 encoded key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str

    :raises UDLRequestError: If the response code is not 200

    :return: The response from the UDL server
    :rtype: Response
    """
    DEWDL_LOG.info(f"Retrieving data from {udl_endpoint.to_string()} using base64 key")
    response = requests.get(udl_endpoint.to_string(), headers={"Authorization": b64_key}, verify=False)
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.GET:
        raise UDLRequestError(response)

    return response


def _get_from_udl_with_cert(udl_endpoint: UDLQuery, cert_path: Path, key_path: Path) -> Response:
    """Performs a GET request to the UDL server using a certificate and key

    :param udl_endpoint: URL of the UDL request
    :type udl_endpoint: str

    :raises UDLRequestError: If the response code is not 200

    :return: The response from the UDL server
    :rtype: Response
    """
    DEWDL_LOG.info(f"Retrieving data from {udl_endpoint.to_string()} crt={cert_path} key={key_path}")
    response = requests.get(udl_endpoint.to_string(), cert=(cert_path.as_posix(), key_path.as_posix()), verify=True)
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.GET:
        raise UDLRequestError(response)

    return response
