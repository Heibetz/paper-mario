"""Enemy model."""
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from config import Base


class Enemy(Base):
    """Enemy characters in the game."""
    
    __tablename__ = "enemies"
    
    # Primary Key
    enemy_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    character_id = Column(
        Integer,
        ForeignKey("characters.character_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    card_score = Column(Integer, nullable=False, default=0)
    
    # Relationships
    character = relationship("Character", back_populates="enemy")
    
    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("hp > 0", name="check_enemy_hp_positive"),  # CHECK constraint
        CheckConstraint("attack >= 0", name="check_enemy_attack_non_negative"),  # CHECK constraint
        CheckConstraint("defense >= 0", name="check_enemy_defense_non_negative"),  # CHECK constraint
        CheckConstraint("card_score >= 0", name="check_card_score_non_negative"),  # CHECK constraint
        Index("idx_enemy_character", "character_id"),  # INDEX on FK
    )
    
    def __repr__(self):
        return f"<Enemy(id={self.enemy_id}, hp={self.hp}, atk={self.attack}, def={self.defense})>"
