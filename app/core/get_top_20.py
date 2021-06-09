import requests
from sqlalchemy.orm import Session

from app.models import models
from app.schemas.schemas import (Character, CharacterList, CharacterSpec, Item,
                                 Items, Top20)

URL = "https://raider.io/api/v1/mythic-plus/runs"
BLIZZARD_API_URL = "https://us.api.blizzard.com/"

# params = {'season-sl-1', 'us', 'de-other-side', 'current', '0'}

dos = Top20(season='season-sl-1',
            region='us',
            dungeon='de-other-side',
            affixes='current',
            page='0')


def get_top_20(top_20: Top20) -> CharacterList:
    character_list = []
    req = requests.get(url=URL, params=top_20)
    req_json = req.json()
    ranks = req_json['rankings']
    for run in ranks:
        for members in run['run']['roster']:
            character_list.append(
                Character(
                    name=(members['character']['name']).lower(),
                    character_class=members['character']['class']['slug'],
                    spec=members['character']['spec']['slug'],
                    realm=members['character']['realm']['slug'],
                    region=members['character']['region']['slug']))

    return CharacterList(characters=character_list)


def get_character_items(character: Character) -> Items:
    """
    https://us.api.blizzard.com/profile/wow/character/hyjal/hiikus/equipment
    :param character:
    :return:
    """
    headers = {"Authorization": "Bearer xxxx"}
    querystring = {"namespace": "profile-us", "locale": "en_US"}
    profile_url = f"{BLIZZARD_API_URL}/profile/wow/character/{character.realm}/{character.name}/equipment"
    payload = ""
    req = requests.get(url=profile_url,
                       params=querystring,
                       headers=headers,
                       data=payload)
    item_list = Items(items=[])
    character_json = req.json()
    if 'equipped_items' not in character_json:
        item_list.items.append(Item())
    else:
        for items in character_json['equipped_items']:
            if 'enchantments' in items:
                for enchants in items['enchantments']:
                    if enchants['enchantment_slot']['type'] != "TEMPORARY":
                        item_list.items.append(
                            Item(name=items['name'],
                                 ilvl=items['level']['value'],
                                 enchantments=enchants['display_string']))
            else:
                item_list.items.append(
                    Item(name=items['name'], ilvl=items['level']['value']))
    return item_list


dos_top_20 = get_top_20(top_20=dos)


def toon_spec(char_list: CharacterList):
    full_char_list = []
    for toons in char_list.characters:
        i = get_character_items(toons)
        full_char_list.append(CharacterSpec(info=toons, items=i))

    return full_char_list


def load_data(db: Session):
    character_list = toon_spec(dos_top_20)
    for toon in character_list:
        character_db = models.Character(
            name=toon.info.name,
            character_class=toon.info.character_class,
            spec=toon.info.spec,
            realm=toon.info.realm,
            region=toon.info.region,
            dungeon="de-other-side")
        db.add(character_db)
        db.commit()
        db.refresh(character_db)
        print(f"added user to character DB: {toon.info}")
        for item in toon.items.items:
            item_db = models.Item(name=item.name,
                                  ilvl=item.ilvl,
                                  enchantments=item.enchantments,
                                  spec=toon.info.spec,
                                  dungeon="de-other-side",
                                  character_class=toon.info.character_class)
            db.add(item_db)
            db.commit()
            db.refresh(item_db)
            print(f"added {item} to item table.")
