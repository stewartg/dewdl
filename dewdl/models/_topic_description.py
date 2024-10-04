from pydantic import BaseModel


class TopicDescription(BaseModel):
    topic: str
    minPos: int
    maxPos: int
    description: str
    partition: int
    udlOpenAPISchema: str
