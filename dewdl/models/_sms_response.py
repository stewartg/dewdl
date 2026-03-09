from pydantic import BaseModel


class SMSResponse(BaseModel):
    data: list[dict]
    next_offset: int
