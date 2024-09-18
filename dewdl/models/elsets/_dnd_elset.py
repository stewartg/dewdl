from dewdl.models.elsets._base_elset import BaseElset


class DNDElset(BaseElset):
    origin: str  # type: ignore
    uct: bool  # type: ignore
    algorithm: str  # type: ignore
    tags: list[str]  # type: ignore
    origObjectId: str  # type: ignore
    ephemType: int  # type: ignore
    descriptor: str  # type: ignore
