from sqlalchemy import (Column, Integer, String)

from app.db.base import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    character_class = Column(String)
    spec = Column(String)
    realm = Column(String)
    region = Column(String)
    dungeon = Column(String)

    class Config:
        orm_mode: True


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ilvl = Column(String)
    enchantments = Column(String)
    spec = Column(String)
    character_class = Column(String)
    dungeon = Column(String)

    class Config:
        orm_mode: True
