"""Navigation Object schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from models.navigation_objects import NavigationType


class NavigationObjectBase(BaseModel):
    """Base navigation object schema."""
    location_id: int
    type: NavigationType
    properties: Optional[str] = None


class NavigationObjectCreate(NavigationObjectBase):
    """Schema for creating a navigation object."""
    pass


class NavigationObjectUpdate(BaseModel):
    """Schema for updating a navigation object."""
    location_id: Optional[int] = None
    type: Optional[NavigationType] = None
    properties: Optional[str] = None


class NavigationObjectResponse(NavigationObjectBase):
    """Schema for navigation object response."""
    navobj_id: int
    
    model_config = ConfigDict(from_attributes=True)
