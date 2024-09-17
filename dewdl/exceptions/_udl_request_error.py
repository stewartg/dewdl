import json

from requests.models import Response  # type: ignore

from dewdl.enums import UDLRequestErrorCode


class UDLRequestError(Exception):
    def __init__(self, response: Response) -> None:

        try:
            status_code = UDLRequestErrorCode(response.status_code)
        except ValueError:
            status_code = response.status_code

        if status_code == UDLRequestErrorCode.INVALID_CREDENTIALS:
            msg = "Invalid credentials for UDL"
        else:
            try:
                msg = json.loads(response.text)["message"]
            except KeyError:
                msg = f"Unexpected response - {response.status_code}"

        super().__init__(f"{msg}")
