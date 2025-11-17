"""Playable Character model."""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from config import Base


class PlayableCharacter(Base):
    """Playable characters that the player can control."""
    
    __tablename__ = "playable_characters"
    
    # Primary Key (also Foreign Key)
    character_id = Column(
        Integer, 
        ForeignKey("characters.character_id", ondelete="CASCADE"),
        primary_key=True
    )
    
    # Foreign Keys
    unlock_chapter_id = Column(
        Integer,
        ForeignKey("chapters.chapter_id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Columns
    special_ability = Column(String(200))
    
    # Relationships
    character = relationship("Character", back_populates="playable")
    unlock_chapter = relationship("Chapter", back_populates="playable_characters")
    
    # Indexes
    __table_args__ = (
        Index("idx_playable_unlock_chapter", "unlock_chapter_id"),  # INDEX on FK
    )
    
    def __repr__(self):
        return f"<PlayableCharacter(id={self.character_id}, ability='{self.special_ability}')>"
