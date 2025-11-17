"""Status Effect schemas."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from models.status_effects import EffectType


class StatusEffectBase(BaseModel):
    """Base status effect schema."""
    name: str
    effect_type: EffectType
    duration_seconds: int = Field(ge=0)


class StatusEffectCreate(StatusEffectBase):
    """Schema for creating a status effect."""
    pass


class StatusEffectUpdate(BaseModel):
    """Schema for updating a status effect."""
    name: Optional[str] = None
    effect_type: Optional[EffectType] = None
    duration_seconds: Optional[int] = Field(None, ge=0)


class StatusEffectResponse(StatusEffectBase):
    """Schema for status effect response."""
    status_id: int
    
    model_config = ConfigDict(from_attributes=True)


# Character Status Effect schemas
class CharacterStatusEffectBase(BaseModel):
    """Base character status effect schema."""
    character_id: int
    status_id: int
    applied_at: datetime
    expires_at: datetime


class CharacterStatusEffectCreate(BaseModel):
    """Schema for creating a character status effect."""
    character_id: int
    status_id: int
    expires_at: datetime


class CharacterStatusEffectResponse(CharacterStatusEffectBase):
    """Schema for character status effect response."""
    
    model_config = ConfigDict(from_attributes=True)
