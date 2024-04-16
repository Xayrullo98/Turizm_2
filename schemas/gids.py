
from pydantic import BaseModel


class GidBase(BaseModel):
    name: str
    phone: str
    address: str
    languages: str

class GidCreate(GidBase):
    pass


class GidUpdate(GidBase):
    id: int

