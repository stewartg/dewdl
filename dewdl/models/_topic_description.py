from pydantic import BaseModel

# ruff: noqa: N815


class TopicDescription(BaseModel):
    topic: str
    minPos: int
    maxPos: int
    description: str
    udlOpenAPISchema: str
