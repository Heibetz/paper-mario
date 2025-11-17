"""Pixl schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PixlBase(BaseModel):
    """Base pixl schema."""
    name: str
    unlock_chapter_id: Optional[int] = None
    ability: Optional[str] = None
    is_optional: bool = False


class PixlCreate(PixlBase):
    """Schema for creating a pixl."""
    pass


class PixlUpdate(BaseModel):
    """Schema for updating a pixl."""
    name: Optional[str] = None
    unlock_chapter_id: Optional[int] = None
    ability: Optional[str] = None
    is_optional: Optional[bool] = None


class PixlResponse(PixlBase):
    """Schema for pixl response."""
    pixl_id: int
    
    model_config = ConfigDict(from_attributes=True)
