from typing import (List, Optional)

from pydantic import BaseModel


class Top20(BaseModel):
    season: str
    region: str
    dungeon: str
    affixes: str
    page: str


class Character(BaseModel):
    name: str
    character_class: str
    spec: str
    realm: str
    region: str


class CharacterList(BaseModel):
    characters: List[Character]


class Item(BaseModel):
    name: Optional[str]
    ilvl: Optional[str]
    enchantments: Optional[str]


class Items(BaseModel):
    items: List[Item]


class CharacterSpec(BaseModel):
    info: Character
    items: Items
