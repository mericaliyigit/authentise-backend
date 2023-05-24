from sqlalchemy import Column, Integer, String, CheckConstraint

from .database import Base


class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    breed = Column(String, nullable=False)
    rank = Column(Integer, CheckConstraint(
        'rank >= 0 AND rank <= 100'), nullable=False)
    type = Column(String, nullable=False)
    img_url = Column(String, nullable=True)
