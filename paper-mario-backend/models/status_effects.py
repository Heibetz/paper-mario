"""Status Effect models."""
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, CheckConstraint, Index, DateTime
from sqlalchemy.orm import relationship
from config import Base
import enum
from datetime import datetime


class EffectType(enum.Enum):
    """Effect type enumeration."""
    buff = "buff"
    debuff = "debuff"


class StatusEffect(Base):
    """Status effects that can be applied to characters."""
    
    __tablename__ = "status_effects"
    
    # Primary Key
    status_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(50), nullable=False, unique=True)  # UNIQUE constraint
    effect_type = Column(Enum(EffectType), nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    
    # Relationships
    character_effects = relationship("CharacterStatusEffect", back_populates="status")
    
    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("duration_seconds >= 0", name="check_duration_non_negative"),  # CHECK constraint
        Index("idx_status_name", "name"),  # INDEX on name
    )
    
    def __repr__(self):
        return f"<StatusEffect(id={self.status_id}, name='{self.name}', type={self.effect_type.value})>"


class CharacterStatusEffect(Base):
    """Join table for Characters and Status Effects."""
    
    __tablename__ = "character_status_effects"
    
    # Composite Primary Key
    character_id = Column(
        Integer,
        ForeignKey("characters.character_id", ondelete="CASCADE"),
        primary_key=True
    )
    status_id = Column(
        Integer,
        ForeignKey("status_effects.status_id", ondelete="CASCADE"),
        primary_key=True
    )
    
    # Columns
    applied_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationships
    character = relationship("Character", back_populates="status_effects")
    status = relationship("StatusEffect", back_populates="character_effects")
    
    # Indexes
    __table_args__ = (
        Index("idx_char_status_character", "character_id"),  # INDEX on FK
        Index("idx_char_status_status", "status_id"),  # INDEX on FK
        Index("idx_char_status_expires", "expires_at"),  # INDEX for expiration queries
    )
    
    def __repr__(self):
        return f"<CharacterStatusEffect(char_id={self.character_id}, status_id={self.status_id})>"
