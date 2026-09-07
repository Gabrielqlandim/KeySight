from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    slug: str
    image_url: str | None = None

class GameRead(GameBase):
    id: int
    
    class Config:
        from_attributes = True

class GameCreate(GameBase):
    pass
    