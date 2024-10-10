from sqlalchemy import Column, Integer, String, Text
from .database import Base

class CachedOutcome(Base):
    __tablename__ = "cached_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    input_hash = Column(String, unique=True, index=True)
    payload = Column(Text)