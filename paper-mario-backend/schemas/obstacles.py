"""Obstacle schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ObstacleBase(BaseModel):
    """Base obstacle schema."""
    location_id: int
    type: str
    behavior: Optional[str] = None


class ObstacleCreate(ObstacleBase):
    """Schema for creating an obstacle."""
    pass


class ObstacleUpdate(BaseModel):
    """Schema for updating an obstacle."""
    location_id: Optional[int] = None
    type: Optional[str] = None
    behavior: Optional[str] = None


class ObstacleResponse(ObstacleBase):
    """Schema for obstacle response."""
    obstacle_id: int
    
    model_config = ConfigDict(from_attributes=True)
