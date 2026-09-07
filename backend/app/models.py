from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=True)

    offers = relationship("StoreOffer", back_populates="game", cascade="all, delete-orphan")

class StoreOffer(Base):
    __tablename__ = "store_offers"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    store_name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    currency = Column(String, default="BRL")
    url = Column(String, nullable=False)

    game = relationship("Game", back_populates="offers")
    price_history = relationship("PriceHistory", back_populates="offer", cascade="all, delete-orphan")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("store_offers.id"), nullable=False)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    offer = relationship("StoreOffer", back_populates="price_history")