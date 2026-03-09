from pydantic import BaseModel

# ruff: noqa: N815


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
    idElset: str | None = None
    origin: str | None = None
    satNo: int | None = None
    uct: bool | None = None
    revNo: int | None = None
    bStar: float | None = None
    agom: float | None = None
    ballisticCoeff: float | None = None
    meanMotionDot: float | None = None
    meanMotionDDot: float | None = None
    semiMajorAxis: float | None = None
    period: float | None = None
    apogee: float | None = None
    perigee: float | None = None
    origObjectId: str | None = None
    descriptor: str | None = None
    rawFileURI: str | None = None
    tags: list[str] | None = None
    algorithm: str | None = None
    sourcedData: list[str] | None = None
    sourcedDataTypes: list[str] | None = None
    transactionId: str | None = None
    ephemType: int | None = None
