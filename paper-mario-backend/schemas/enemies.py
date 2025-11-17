"""Enemy schemas."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class EnemyBase(BaseModel):
    """Base enemy schema."""
    character_id: int
    hp: int = Field(gt=0, description="HP must be positive")
    attack: int = Field(ge=0, description="Attack cannot be negative")
    defense: int = Field(ge=0, description="Defense cannot be negative")
    card_score: int = Field(ge=0, default=0)


class EnemyCreate(EnemyBase):
    """Schema for creating an enemy."""
    pass


class EnemyUpdate(BaseModel):
    """Schema for updating an enemy."""
    hp: Optional[int] = Field(None, gt=0)
    attack: Optional[int] = Field(None, ge=0)
    defense: Optional[int] = Field(None, ge=0)
    card_score: Optional[int] = Field(None, ge=0)


class EnemyResponse(EnemyBase):
    """Schema for enemy response."""
    enemy_id: int
    
    model_config = ConfigDict(from_attributes=True)
