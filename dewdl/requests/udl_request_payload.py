from dataclasses import dataclass
from pathlib import Path

from dewdl.udl_actions import UDLBaseAction


@dataclass
class UDLRequestPayload:
    endpoint: UDLBaseAction
    method: str = "GET"
    post_body: dict | None = None
    zip_data: bytes | None = None
    token: str | None = None
    b64_key: str | None = None
    crt: Path | None = None
    key: Path | None = None
    async_flag: bool = False
    is_filedrop: bool = False
