"""Chapter model."""
from sqlalchemy import Column, Integer, String, Text, CheckConstraint, Index
from sqlalchemy.orm import relationship
from config import Base


class Chapter(Base):
    """Chapters/Worlds in the game."""
    
    __tablename__ = "chapters"
    
    # Primary Key
    chapter_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(100), nullable=False, unique=True)  # UNIQUE constraint
    world_number = Column(Integer, nullable=False)
    description = Column(Text)
    
    # Relationships
    locations = relationship("Location", back_populates="chapter")
    playable_characters = relationship("PlayableCharacter", back_populates="unlock_chapter")
    pixls = relationship("Pixl", back_populates="unlock_chapter")
    bosses = relationship("Boss", back_populates="chapter")
    
    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("world_number > 0", name="check_world_number_positive"),  # CHECK constraint
        Index("idx_chapter_world_number", "world_number"),  # INDEX on world_number
    )
    
    def __repr__(self):
        return f"<Chapter(id={self.chapter_id}, name='{self.name}', world={self.world_number})>"
