"""Pydantic schemas for database views."""
from pydantic import BaseModel
from typing import Optional


class EnemyDetailsResponse(BaseModel):
    """Response schema for enemy details view."""
    enemy_id: int
    hp: int
    attack: int
    defense: int
    card_score: int
    character_id: int
    character_name: str
    description: Optional[str]
    
    class Config:
        from_attributes = True


class BossDetailsResponse(BaseModel):
    """Response schema for boss details view."""
    boss_id: int
    character_id: int
    chapter_id: int
    phase_count: int
    special_mechanics: Optional[str]
    boss_name: str
    boss_description: Optional[str]
    chapter_name: str
    world_number: int
    
    class Config:
        from_attributes = True


class LocationSummaryResponse(BaseModel):
    """Response schema for location summary view."""
    location_id: int
    location_name: str
    location_type: str
    description: Optional[str]
    chapter_id: int
    chapter_name: str
    world_number: int
    object_count: int
    block_count: int
    nav_object_count: int
    obstacle_count: int
    switch_count: int
    
    class Config:
        from_attributes = True


class PlayableCharacterDetailsResponse(BaseModel):
    """Response schema for playable character details view."""
    character_id: int
    character_name: str
    description: Optional[str]
    special_ability: Optional[str]
    unlock_chapter_id: Optional[int]
    unlock_chapter_name: Optional[str]
    unlock_world: Optional[int]
    
    class Config:
        from_attributes = True


class BlockInventoryResponse(BaseModel):
    """Response schema for block inventory view."""
    block_id: int
    block_type: str
    properties: Optional[str]
    location_id: int
    location_name: str
    location_type: str
    chapter_name: str
    world_number: int
    contains_item_id: Optional[int]
    item_name: Optional[str]
    is_key_item: Optional[bool]
    item_effect: Optional[str]
    
    class Config:
        from_attributes = True


class QuestOverviewResponse(BaseModel):
    """Response schema for quest overview view."""
    quest_id: int
    quest_name: str
    description: Optional[str]
    start_location_id: Optional[int]
    start_location_name: Optional[str]
    chapter_name: Optional[str]
    reward_item_id: Optional[int]
    reward_item_name: Optional[str]
    reward_is_key_item: Optional[bool]
    
    class Config:
        from_attributes = True


class ChapterStatisticsResponse(BaseModel):
    """Response schema for chapter statistics view."""
    chapter_id: int
    chapter_name: str
    world_number: int
    description: Optional[str]
    location_count: int
    boss_count: int
    pixl_count: int
    playable_character_count: int
    
    class Config:
        from_attributes = True
