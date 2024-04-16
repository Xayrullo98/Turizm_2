import typing

from pydantic import BaseModel
from schemas.texts import textsBase
from schemas.videos import videosBase
from pydantic import ConfigDict


class AboutBase(BaseModel):
    texts: typing.List[textsBase]
    videos: typing.List[videosBase]





class textsUpdate(textsBase):
    id: int
