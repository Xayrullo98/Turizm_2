from pydantic import BaseModel


class videosBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class videosUpdate(videosBase):
    id: int
