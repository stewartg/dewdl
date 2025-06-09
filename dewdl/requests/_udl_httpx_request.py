import json
from pathlib import Path
from typing import Optional, Union

import httpx
from pydantic import BaseModel, ConfigDict

from dewdl import DEWDL_LOG, DewDLConfigs
from dewdl.enums import UDLRequestSuccessCode
from dewdl.exceptions import UDLRequestError
from dewdl.requests.udl_request_payload import UDLRequestPayload
from dewdl.udl_actions import UDLBaseAction, UDLFileDrop, UDLQuery


class UDLRequest:
    @staticmethod
    def format_booleans(input_str: str) -> str:
        """Converts the string 'True' to 'true' and 'False' to 'false'.

        :param input_str: The string to convert
        """
        return input_str.replace("True", "true").replace("False", "false")

    @staticmethod
    def _get_configs():
        token = b64_key = crt = key = None
        if DewDLConfigs.has_token():
            token = DewDLConfigs.get_token()
        if DewDLConfigs.has_user() and DewDLConfigs.has_password():
            b64_key = DewDLConfigs.get_b64_key()
        if DewDLConfigs.has_cert() and DewDLConfigs.has_key():
            crt, key = DewDLConfigs.get_crt_path(), DewDLConfigs.get_key_path()
        return token, b64_key, crt, key

    @staticmethod
    def get(udl_endpoint: UDLQuery, async_flag: bool = False) -> httpx.Response:
        token, b64_key, crt, key = UDLRequest._get_configs()
        payload = UDLRequestPayload(
            endpoint=udl_endpoint, token=token, b64_key=b64_key, crt=crt, key=key, async_flag=async_flag
        )
        return UDLRequest._make_request(payload=payload)

    @staticmethod
    def post(udl_endpoint: UDLQuery, post_data: Union[dict, bytes], async_flag: bool = False) -> str:
        token, b64_key, crt, key = UDLRequest._get_configs()
        payload = UDLRequestPayload(
            endpoint=udl_endpoint,
            method="POST",
            post_body=post_data if isinstance(post_data, dict) else None,
            zip_data=post_data if isinstance(post_data, bytes) else None,
            token=token,
            b64_key=b64_key,
            crt=crt,
            key=key,
            async_flag=async_flag,
        )
        return UDLRequest._make_request(payload=payload)

    @staticmethod
    def filedrop(udl_endpoint: UDLFileDrop, post_body: list[dict], async_flag: bool = False) -> None:
        token, b64_key, crt, key = UDLRequest._get_configs()
        payload = UDLRequestPayload(
            endpoint=udl_endpoint,
            method="POST",
            token=token,
            b64_key=b64_key,
            crt=crt,
            key=key,
            post_body=post_body,
            async_flag=async_flag,
            is_filedrop=True,
        )
        return UDLRequest._make_request(payload=payload)

    @staticmethod
    def _make_request(payload: UDLRequestPayload) -> httpx.Response:
        cert = UDLRequest._check_cert(payload.crt, payload.key)
        response_func, httpx_client = UDLRequest._method_to_func(cert, payload.method, payload.async_flag)
        request_args = {"udl_endpoint": payload.endpoint}
        headers = {}
        if payload.token:
            auth_header_value = payload.token
        elif payload.b64_key:
            auth_header_value = payload.b64_key
        else:
            auth_header_value = None
        if auth_header_value:
            headers["Authorization"] = auth_header_value
        if payload.method == "POST":
            UDLRequest._setup_post_params(payload, request_args, headers)

        DEWDL_LOG.info(
            f"Publishing to {payload.endpoint.to_string()} using {'token' if payload.token else 'b64_key' if payload.b64_key else 'cert'}"
        )
        if payload.async_flag:
            request_args["client"] = httpx_client
            return response_func(**request_args)
        with httpx_client as client:
            request_args["client"] = client
            return response_func(**request_args)

    @staticmethod
    def _check_cert(crt: Optional[Path] = None, key: Optional[Path] = None):
        cert = None
        if crt and key:
            crt_posix = crt.as_posix() if hasattr(crt, "as_posix") else str(crt)
            key_posix = key.as_posix() if hasattr(key, "as_posix") else str(key)
            cert = (crt_posix, key_posix)
        return cert

    @staticmethod
    def _method_to_func(cert: tuple, method: str, async_flag: bool):
        method_to_func_map = {
            ("POST", True): (
                _post_to_udl_async,
                httpx.AsyncClient(cert=cert, verify=True) if cert else httpx.AsyncClient(),
            ),
            ("POST", False): (_post_to_udl, httpx.Client(cert=cert, verify=True) if cert else httpx.Client()),
            ("GET", True): (
                _get_udl_response_async,
                httpx.AsyncClient(cert=cert, verify=True) if cert else httpx.AsyncClient(),
            ),
            ("GET", False): (_get_udl_response, httpx.Client(cert=cert, verify=True) if cert else httpx.Client()),
        }
        # Retrieve the appropriate function/httpx client based on method and async_flag
        mtf = method_to_func_map.get((method, async_flag))
        return mtf[0], mtf[1]

    @staticmethod
    def _setup_post_params(payload, request_args, headers):
        data = None
        if payload.post_body:
            headers.update({**UDLRequest.accept_json(), **UDLRequest.content_json()})
            json_str = json.dumps(payload.post_body)
            data = UDLRequest.format_booleans(json_str)
        elif payload.zip_data:
            data = payload.zip_data
            headers.update({**UDLRequest.accept_zip(), **UDLRequest.content_zip()})
        request_args["headers"] = headers
        request_args["post_data"] = data
        request_args["is_filedrop"] = payload.is_filedrop

    @staticmethod
    def accept_json() -> dict:
        """Gets the accept_json header."""
        return {"accept": "application/json"}

    @staticmethod
    def content_json() -> dict:
        """Gets the content_json header."""
        return {"content-type": "application/json"}

    @staticmethod
    def accept_zip() -> dict:
        """Gets the accept_zip header."""
        return {"accept": "application/zip"}

    @staticmethod
    def content_zip() -> dict:
        """Gets the content_zip header."""
        return {"content-type": "application/zip"}

    class Payload(BaseModel):
        method: str = "GET"
        post_body: Optional[dict] = None
        zip_data: Optional[bytes] = None
        token: Optional[str] = None
        b64_key: Optional[str] = None
        crt: Optional[Path] = None
        key: Optional[Path] = None
        async_flag: bool = False
        is_filedrop: bool = False

        model_config = ConfigDict(arbitrary_types_allowed=True)


async def _get_udl_response_async(udl_endpoint: UDLBaseAction, client: httpx.AsyncClient) -> httpx.Response:
    response = await client.get(udl_endpoint.to_string(), timeout=30)
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.GET:
        raise UDLRequestError(response)
    return response


def _get_udl_response(udl_endpoint: UDLBaseAction, client: httpx.Client) -> httpx.Response:
    response = client.get(udl_endpoint.to_string(), timeout=30)
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.GET:
        raise UDLRequestError(response)
    return response


async def _post_to_udl_async(
    udl_endpoint: UDLBaseAction,
    post_data: Union[str, bytes],
    client: httpx.AsyncClient,
    headers: dict = None,
    is_filedrop: bool = False,
) -> str:
    response = await client.post(udl_endpoint.to_string(), headers=headers, data=post_data, timeout=30)
    if is_filedrop:
        resp_str = _verify_post(response)
    else:
        _verify_post(response)
        resp_str = _get_post_location(response)
    return resp_str


def _post_to_udl(
    udl_endpoint: UDLBaseAction,
    post_data: Union[str, bytes],
    client: httpx.Client,
    headers: dict = None,
    is_filedrop: bool = False,
) -> str:
    response = client.post(udl_endpoint.to_string(), headers=headers, data=post_data, timeout=30)
    if is_filedrop:
        resp_str = _verify_filedrop(response)
    else:
        _verify_post(response)
        resp_str = _get_post_location(response)
    return resp_str


def _verify_post(response: httpx.Response) -> str:
    # check for successful post
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.POST:
        raise UDLRequestError(response)
    return response.text


def _verify_filedrop(response: httpx.Response) -> str:
    # check for successful filedrop
    try:
        success_code = UDLRequestSuccessCode(response.status_code)
    except ValueError:
        success_code = response.status_code
    if success_code != UDLRequestSuccessCode.FILEDROP:
        raise UDLRequestError(response)
    return response.text


def _get_post_location(response: httpx.Response) -> str:
    # check for location of newly posted data
    url = response.headers.get("location")
    if url is None:
        raise KeyError("No UUID returned from UDL")
    # parse the UUID from the URL
    return url.split("/")[-1]
