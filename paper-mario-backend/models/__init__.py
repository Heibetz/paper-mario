"""Models package for Paper Mario database."""
from .characters import Character
from .playable_characters import PlayableCharacter
from .chapters import Chapter
from .locations import Location
from .pixls import Pixl
from .status_effects import StatusEffect, CharacterStatusEffect
from .enemies import Enemy
from .bosses import Boss
from .items import Item
from .objects import Object
from .navigation_objects import NavigationObject
from .obstacles import Obstacle
from .blocks_containers import BlockContainer
from .switches import Switch
from .side_quests import SideQuest, QuestCharacter

__all__ = [
    "Character",
    "PlayableCharacter",
    "Chapter",
    "Location",
    "Pixl",
    "StatusEffect",
    "CharacterStatusEffect",
    "Enemy",
    "Boss",
    "Item",
    "Object",
    "NavigationObject",
    "Obstacle",
    "BlockContainer",
    "Switch",
    "SideQuest",
    "QuestCharacter",
]
