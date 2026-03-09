from typing import Optional, Union

from pydantic import BaseModel

# ruff: noqa: N815


class Notification(BaseModel):
    classificationMarking: str
    msgType: str
    msgBody: str | dict
    dataMode: str
    source: str
    origin: str | None = None
    id: str | None = None
