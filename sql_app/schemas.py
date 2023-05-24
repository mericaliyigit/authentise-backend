from pydantic import BaseModel, Field, AnyUrl


class Pet(BaseModel):
    name: str
    breed: str
    rank: int = Field(..., ge=0, le=100)
    type: str
    img_url: AnyUrl | None = None

    class Config:
        orm_mode = True
