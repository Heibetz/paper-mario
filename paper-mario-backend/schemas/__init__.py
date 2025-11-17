"""Pydantic schemas for API request/response validation."""
from .characters import CharacterBase, CharacterCreate, CharacterResponse
from .chapters import ChapterBase, ChapterCreate, ChapterResponse
from .enemies import EnemyBase, EnemyCreate, EnemyResponse
from .items import ItemBase, ItemCreate, ItemResponse
from .side_quests import SideQuestBase, SideQuestCreate, SideQuestResponse
from .playable_characters import PlayableCharacterBase, PlayableCharacterCreate, PlayableCharacterResponse
from .locations import LocationBase, LocationCreate, LocationResponse
from .pixls import PixlBase, PixlCreate, PixlResponse
from .status_effects import StatusEffectBase, StatusEffectCreate, StatusEffectResponse
from .bosses import BossBase, BossCreate, BossResponse
from .objects import ObjectBase, ObjectCreate, ObjectResponse
from .navigation_objects import NavigationObjectBase, NavigationObjectCreate, NavigationObjectResponse
from .obstacles import ObstacleBase, ObstacleCreate, ObstacleResponse
from .blocks_containers import BlockContainerBase, BlockContainerCreate, BlockContainerResponse
from .switches import SwitchBase, SwitchCreate, SwitchResponse

__all__ = [
    "CharacterBase",
    "CharacterCreate",
    "CharacterResponse",
    "ChapterBase",
    "ChapterCreate",
    "ChapterResponse",
    "EnemyBase",
    "EnemyCreate",
    "EnemyResponse",
    "ItemBase",
    "ItemCreate",
    "ItemResponse",
    "SideQuestBase",
    "SideQuestCreate",
    "SideQuestResponse",
    "PlayableCharacterBase",
    "PlayableCharacterCreate",
    "PlayableCharacterResponse",
    "LocationBase",
    "LocationCreate",
    "LocationResponse",
    "PixlBase",
    "PixlCreate",
    "PixlResponse",
    "StatusEffectBase",
    "StatusEffectCreate",
    "StatusEffectResponse",
    "BossBase",
    "BossCreate",
    "BossResponse",
    "ObjectBase",
    "ObjectCreate",
    "ObjectResponse",
    "NavigationObjectBase",
    "NavigationObjectCreate",
    "NavigationObjectResponse",
    "ObstacleBase",
    "ObstacleCreate",
    "ObstacleResponse",
    "BlockContainerBase",
    "BlockContainerCreate",
    "BlockContainerResponse",
    "SwitchBase",
    "SwitchCreate",
    "SwitchResponse",
]
