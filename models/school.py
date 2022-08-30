from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, index=True)
    dbn = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    items = relationship("Item", back_populates="owner")
