"""Character schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CharacterBase(BaseModel):
    """Base character schema."""
    name: str
    description: Optional[str] = None


class CharacterCreate(CharacterBase):
    """Schema for creating a character."""
    pass


class CharacterUpdate(BaseModel):
    """Schema for updating a character."""
    name: Optional[str] = None
    description: Optional[str] = None


class CharacterResponse(CharacterBase):
    """Schema for character response."""
    character_id: int
    
    model_config = ConfigDict(from_attributes=True)
