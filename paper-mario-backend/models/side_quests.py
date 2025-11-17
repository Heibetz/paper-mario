"""Side Quest models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from config import Base
import enum


class QuestRole(enum.Enum):
    """Quest character role enumeration."""
    giver = "giver"
    target = "target"
    helper = "helper"


class SideQuest(Base):
    """Side quests in the game."""
    
    __tablename__ = "side_quests"
    
    # Primary Key
    quest_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(100), nullable=False, unique=True)  # UNIQUE constraint
    description = Column(Text)
    
    # Foreign Keys
    start_location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="SET NULL"),
        nullable=True
    )
    reward_item_id = Column(
        Integer,
        ForeignKey("items.item_id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Relationships
    start_location = relationship("Location", back_populates="side_quests")
    reward_item = relationship("Item", back_populates="side_quests")
    characters = relationship("QuestCharacter", back_populates="quest")
    
    # Indexes
    __table_args__ = (
        Index("idx_quest_location", "start_location_id"),  # INDEX on FK
        Index("idx_quest_reward", "reward_item_id"),  # INDEX on FK
        Index("idx_quest_name", "name"),  # INDEX on name for searches
    )
    
    def __repr__(self):
        return f"<SideQuest(id={self.quest_id}, name='{self.name}')>"


class QuestCharacter(Base):
    """Join table for Side Quests and Characters."""
    
    __tablename__ = "quest_character"
    
    # Composite Primary Key
    quest_id = Column(
        Integer,
        ForeignKey("side_quests.quest_id", ondelete="CASCADE"),
        primary_key=True
    )
    character_id = Column(
        Integer,
        ForeignKey("characters.character_id", ondelete="CASCADE"),
        primary_key=True
    )
    
    # Columns
    role = Column(Enum(QuestRole), nullable=False)
    
    # Relationships
    quest = relationship("SideQuest", back_populates="characters")
    character = relationship("Character", back_populates="quests")
    
    # Indexes
    __table_args__ = (
        Index("idx_quest_char_quest", "quest_id"),  # INDEX on FK
        Index("idx_quest_char_character", "character_id"),  # INDEX on FK
        Index("idx_quest_char_role", "role"),  # INDEX on role for filtering
    )
    
    def __repr__(self):
        return f"<QuestCharacter(quest_id={self.quest_id}, char_id={self.character_id}, role={self.role.value})>"
