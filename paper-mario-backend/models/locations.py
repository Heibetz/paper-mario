"""Location model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from config import Base
import enum


class LocationType(enum.Enum):
    """Location type enumeration."""
    hub = "hub"
    level = "level"
    dungeon = "dungeon"
    other = "other"


class Location(Base):
    """Game locations/areas."""
    
    __tablename__ = "locations"
    
    # Primary Key
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    chapter_id = Column(
        Integer,
        ForeignKey("chapters.chapter_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    name = Column(String(100), nullable=False)
    type = Column(Enum(LocationType), nullable=False)
    description = Column(Text)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="locations")
    objects = relationship("Object", back_populates="location")
    navigation_objects = relationship("NavigationObject", back_populates="location")
    obstacles = relationship("Obstacle", back_populates="location")
    blocks = relationship("BlockContainer", back_populates="location")
    switches = relationship("Switch", back_populates="location")
    side_quests = relationship("SideQuest", back_populates="start_location")
    
    # Indexes
    __table_args__ = (
        Index("idx_location_chapter", "chapter_id"),  # INDEX on FK
        Index("idx_location_name", "name"),  # INDEX for searches
        Index("idx_location_type", "type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<Location(id={self.location_id}, name='{self.name}', type={self.type.value})>"
