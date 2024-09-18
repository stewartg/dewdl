from pydantic import BaseModel


class DNDNearGeoBody(BaseModel):
    geoScore: float
    tleLine1: str
    tleLine2: str
    name: str
