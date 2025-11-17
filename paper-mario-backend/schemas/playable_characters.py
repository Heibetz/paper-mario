"""Playable Character schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlayableCharacterBase(BaseModel):
    """Base playable character schema."""
    character_id: int
    unlock_chapter_id: Optional[int] = None
    special_ability: Optional[str] = None


class PlayableCharacterCreate(PlayableCharacterBase):
    """Schema for creating a playable character."""
    pass


class PlayableCharacterUpdate(BaseModel):
    """Schema for updating a playable character."""
    unlock_chapter_id: Optional[int] = None
    special_ability: Optional[str] = None


class PlayableCharacterResponse(PlayableCharacterBase):
    """Schema for playable character response."""
    
    model_config = ConfigDict(from_attributes=True)
