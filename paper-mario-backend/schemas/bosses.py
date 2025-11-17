"""Boss schemas."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class BossBase(BaseModel):
    """Base boss schema."""
    character_id: int
    chapter_id: int
    phase_count: int = Field(gt=0, default=1)
    special_mechanics: Optional[str] = None


class BossCreate(BossBase):
    """Schema for creating a boss."""
    pass


class BossUpdate(BaseModel):
    """Schema for updating a boss."""
    chapter_id: Optional[int] = None
    phase_count: Optional[int] = Field(None, gt=0)
    special_mechanics: Optional[str] = None


class BossResponse(BossBase):
    """Schema for boss response."""
    boss_id: int
    
    model_config = ConfigDict(from_attributes=True)
