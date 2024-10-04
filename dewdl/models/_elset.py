from typing import Optional

from pydantic import BaseModel


class Elset(BaseModel):
    source: str
    classificationMarking: str
    dataMode: str
    epoch: str
    meanMotion: float
    eccentricity: float
    inclination: float
    raan: float
    argOfPerigee: float
    meanAnomaly: float
    idElset: Optional[str] = None
    origin: Optional[str] = None
    satNo: Optional[int] = None
    uct: Optional[bool] = None
    revNo: Optional[int] = None
    bStar: Optional[float] = None
    agom: Optional[float] = None
    ballisticCoeff: Optional[float] = None
    meanMotionDot: Optional[float] = None
    meanMotionDDot: Optional[float] = None
    semiMajorAxis: Optional[float] = None
    period: Optional[float] = None
    apogee: Optional[float] = None
    perigee: Optional[float] = None
    origObjectId: Optional[str] = None
    descriptor: Optional[str] = None
    rawFileURI: Optional[str] = None
    tags: Optional[list[str]] = None
    algorithm: Optional[str] = None
    sourcedData: Optional[list[str]] = None
    sourcedDataTypes: Optional[list[str]] = None
    transactionId: Optional[str] = None
    ephemType: Optional[int] = None
