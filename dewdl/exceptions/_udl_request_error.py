import json

from requests.models import Response  # type: ignore

from dewdl.enums import UDLRequestErrorCode


class UDLRequestError(Exception):
    def __init__(self, response: Response) -> None:

        try:
            status_code = UDLRequestErrorCode(response.status_code)
        except ValueError:
            status_code = UDLRequestErrorCode.UNKNOWN

        if status_code == UDLRequestErrorCode.INVALID_CREDENTIALS:
            msg = f"{status_code.value} Unauthorized - Verify credentials and try again."
        else:
            try:
                msg = f'{response.status_code} - {json.loads(response.text)["message"]}'
            except KeyError:
                msg = f"{response.status_code} - Unexpected response"

        super().__init__(f"{msg}")
