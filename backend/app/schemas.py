from pydantic import BaseModel
from datetime import datetime

class StoreOfferRead(BaseModel):
    id: int
    store_name: str
    current_price: float
    currency: str
    url: str

    class Config:
        from_attributes = True

class PricePoint(BaseModel):
    price: float
    recorded_at: datetime

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
    