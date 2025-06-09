from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict

from dewdl.udl_actions import UDLBaseAction


class UDLRequestPayload(BaseModel):
    method: str = "GET"
    endpoint: UDLBaseAction
    post_body: Optional[dict] = None
    zip_data: Optional[bytes] = None
    token: Optional[str] = None
    b64_key: Optional[str] = None
    crt: Optional[Path] = None
    key: Optional[Path] = None
    async_flag: bool = False
    is_filedrop: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)
