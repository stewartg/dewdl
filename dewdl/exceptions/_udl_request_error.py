import json

from requests.models import Response  # type: ignore


class UDLRequestError(Exception):
    def __init__(self, response: Response) -> None:

        if response.status_code == 401:
            msg = "Invalid credentials for UDL"
        else:
            try:
                msg = json.loads(response.text)["message"]
            except KeyError:
                msg = f"Unexpected response - {response.status_code}"

        super().__init__(f"{msg}")
