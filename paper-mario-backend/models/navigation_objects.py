"""Navigation Object model."""
from sqlalchemy import Column, Integer, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from config import Base
import enum


class NavigationType(enum.Enum):
    """Navigation object type enumeration."""
    door = "door"
    arrow = "arrow"
    elevator = "elevator"
    save_block = "save_block"
    star_block = "star_block"
    rift = "rift"


class NavigationObject(Base):
    """Navigation objects in locations (doors, elevators, etc.)."""
    
    __tablename__ = "navigation_objects"
    
    # Primary Key
    navobj_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    type = Column(Enum(NavigationType), nullable=False)
    properties = Column(Text)
    
    # Relationships
    location = relationship("Location", back_populates="navigation_objects")
    switches = relationship("Switch", back_populates="target_navobj")
    
    # Indexes
    __table_args__ = (
        Index("idx_navobj_location", "location_id"),  # INDEX on FK
        Index("idx_navobj_type", "type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<NavigationObject(id={self.navobj_id}, type={self.type.value})>"
