"""Character model."""
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import relationship
from config import Base


class Character(Base):
    """Base Character table for all game characters."""
    
    __tablename__ = "characters"
    
    # Primary Key
    character_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(100), nullable=False, unique=True)  # UNIQUE constraint
    description = Column(Text)
    
    # Relationships
    playable = relationship("PlayableCharacter", back_populates="character", uselist=False)
    enemy = relationship("Enemy", back_populates="character", uselist=False)
    boss = relationship("Boss", back_populates="character", uselist=False)
    status_effects = relationship("CharacterStatusEffect", back_populates="character")
    quests = relationship("QuestCharacter", back_populates="character")
    
    # Indexes
    __table_args__ = (
        Index("idx_character_name", "name"),  # INDEX on name for searches
    )
    
    def __repr__(self):
        return f"<Character(id={self.character_id}, name='{self.name}')>"
