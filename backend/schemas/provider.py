from pydantic import BaseModel
from typing import Optional

class ProviderBase(BaseModel):
    name: str
    category: str
    address: str
    latitude: float
    longitude: float
    rating: float = 0.0
    user_ratings_total: int = 0
    phone: Optional[str] = None
    is_mock: bool = False

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
