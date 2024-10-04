from typing import Optional, Union

from pydantic import BaseModel


class Notification(BaseModel):
    classificationMarking: str
    msgType: str
    msgBody: Union[str, dict]
    dataMode: str
    source: str
    origin: Optional[str] = None
    id: Optional[str] = None
