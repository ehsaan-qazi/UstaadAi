from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)  # plumber, electrician, ac_repair, etc.
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float, default=0.0)
    user_ratings_total = Column(Integer, default=0)
    phone = Column(String, nullable=True)
    is_mock = Column(Boolean, default=False)
