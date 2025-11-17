"""Chapter schemas."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ChapterBase(BaseModel):
    """Base chapter schema."""
    name: str
    world_number: int = Field(gt=0, description="World number must be positive")
    description: Optional[str] = None


class ChapterCreate(ChapterBase):
    """Schema for creating a chapter."""
    pass


class ChapterUpdate(BaseModel):
    """Schema for updating a chapter."""
    name: Optional[str] = None
    world_number: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None


class ChapterResponse(ChapterBase):
    """Schema for chapter response."""
    chapter_id: int
    
    model_config = ConfigDict(from_attributes=True)
