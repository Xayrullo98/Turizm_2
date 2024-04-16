from pydantic import BaseModel

from pydantic import ConfigDict


class textsBase(BaseModel):
    text: str
    language: str


class textsUpdate(textsBase):
    id: int
