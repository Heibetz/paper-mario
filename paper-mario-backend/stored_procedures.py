"""Stored procedures - Complex database operations with transactions."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from models import (
    Character, Enemy, PlayableCharacter, Boss, Chapter,
    Item, BlockContainer, Location, SideQuest, QuestCharacter,
    StatusEffect, CharacterStatusEffect, Pixl
)
from models.side_quests import QuestRole
from models.status_effects import EffectType


class StoredProcedures:
    """Collection of stored procedure-like functions for complex database operations."""
    
    @staticmethod
    def create_enemy_with_character(
        db: Session,
        name: str,
        description: str,
        hp: int,
        attack: int,
        defense: int,
        card_score: int
    ) -> Dict:
        """
        Stored Procedure: Create an enemy with its character in one transaction.
        
        Steps:
        1. Create Character record
        2. Create Enemy record linked to character
        3. Commit both or rollback on error
        
        Returns: Dict with character_id and enemy_id
        """
        try:
            # Step 1: Create character
            character = Character(
                name=name,
                description=description
            )
            db.add(character)
            db.flush()  # Get character_id without committing
            
            # Step 2: Create enemy
            enemy = Enemy(
                character_id=character.character_id,
                hp=hp,
                attack=attack,
                defense=defense,
                card_score=card_score
            )
            db.add(enemy)
            db.commit()
            
            return {
                "success": True,
                "character_id": character.character_id,
                "enemy_id": enemy.enemy_id,
                "message": f"Enemy '{name}' created successfully"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create enemy"
            }
    
    @staticmethod
    def create_boss_with_character(
        db: Session,
        name: str,
        description: str,
        chapter_id: int,
        phase_count: int,
        special_mechanics: Optional[str] = None
    ) -> Dict:
        """
        Stored Procedure: Create a boss with its character in one transaction.
        
        Steps:
        1. Validate chapter exists
        2. Create Character record
        3. Create Boss record
        4. Commit or rollback
        """
        try:
            # Validate chapter
            chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
            if not chapter:
                return {
                    "success": False,
                    "error": f"Chapter {chapter_id} not found"
                }
            
            # Create character
            character = Character(name=name, description=description)
            db.add(character)
            db.flush()
            
            # Create boss
            boss = Boss(
                character_id=character.character_id,
                chapter_id=chapter_id,
                phase_count=phase_count,
                special_mechanics=special_mechanics
            )
            db.add(boss)
            db.commit()
            
            return {
                "success": True,
                "character_id": character.character_id,
                "boss_id": boss.boss_id,
                "chapter": chapter.name,
                "message": f"Boss '{name}' created in {chapter.name}"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def create_side_quest_with_characters(
        db: Session,
        quest_name: str,
        description: str,
        start_location_id: Optional[int],
        reward_item_id: Optional[int],
        quest_giver_id: Optional[int] = None,
        quest_target_id: Optional[int] = None,
        quest_helper_ids: Optional[List[int]] = None
    ) -> Dict:
        """
        Stored Procedure: Create a side quest with all related characters.
        
        Steps:
        1. Validate location and reward item
        2. Create SideQuest record
        3. Add quest giver (if provided)
        4. Add quest target (if provided)
        5. Add quest helpers (if provided)
        6. Commit all or rollback
        """
        try:
            # Validate location
            if start_location_id:
                location = db.query(Location).filter(
                    Location.location_id == start_location_id
                ).first()
                if not location:
                    return {"success": False, "error": f"Location {start_location_id} not found"}
            
            # Validate reward item
            if reward_item_id:
                item = db.query(Item).filter(Item.item_id == reward_item_id).first()
                if not item:
                    return {"success": False, "error": f"Item {reward_item_id} not found"}
            
            # Create quest
            quest = SideQuest(
                name=quest_name,
                description=description,
                start_location_id=start_location_id,
                reward_item_id=reward_item_id
            )
            db.add(quest)
            db.flush()
            
            characters_added = []
            
            # Add quest giver
            if quest_giver_id:
                char = db.query(Character).filter(
                    Character.character_id == quest_giver_id
                ).first()
                if char:
                    qc = QuestCharacter(
                        quest_id=quest.quest_id,
                        character_id=quest_giver_id,
                        role=QuestRole.GIVER
                    )
                    db.add(qc)
                    characters_added.append({"name": char.name, "role": "giver"})
            
            # Add quest target
            if quest_target_id:
                char = db.query(Character).filter(
                    Character.character_id == quest_target_id
                ).first()
                if char:
                    qc = QuestCharacter(
                        quest_id=quest.quest_id,
                        character_id=quest_target_id,
                        role=QuestRole.TARGET
                    )
                    db.add(qc)
                    characters_added.append({"name": char.name, "role": "target"})
            
            # Add quest helpers
            if quest_helper_ids:
                for helper_id in quest_helper_ids:
                    char = db.query(Character).filter(
                        Character.character_id == helper_id
                    ).first()
                    if char:
                        qc = QuestCharacter(
                            quest_id=quest.quest_id,
                            character_id=helper_id,
                            role=QuestRole.HELPER
                        )
                        db.add(qc)
                        characters_added.append({"name": char.name, "role": "helper"})
            
            db.commit()
            
            return {
                "success": True,
                "quest_id": quest.quest_id,
                "quest_name": quest_name,
                "characters_added": characters_added,
                "message": f"Quest '{quest_name}' created with {len(characters_added)} characters"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def apply_status_effect_to_character(
        db: Session,
        character_id: int,
        status_id: int,
        duration_seconds: int
    ) -> Dict:
        """
        Stored Procedure: Apply a status effect to a character.
        
        Steps:
        1. Validate character exists
        2. Validate status effect exists
        3. Check if effect already applied
        4. Create or update CharacterStatusEffect
        5. Commit or rollback
        """
        try:
            # Validate character
            character = db.query(Character).filter(
                Character.character_id == character_id
            ).first()
            if not character:
                return {"success": False, "error": f"Character {character_id} not found"}
            
            # Validate status effect
            status = db.query(StatusEffect).filter(
                StatusEffect.status_id == status_id
            ).first()
            if not status:
                return {"success": False, "error": f"Status effect {status_id} not found"}
            
            # Check if already applied
            existing = db.query(CharacterStatusEffect).filter(
                CharacterStatusEffect.character_id == character_id,
                CharacterStatusEffect.status_id == status_id
            ).first()
            
            now = datetime.utcnow()
            expires_at = now + timedelta(seconds=duration_seconds)
            
            if existing:
                # Update expiration
                existing.expires_at = expires_at
                action = "updated"
            else:
                # Create new
                char_status = CharacterStatusEffect(
                    character_id=character_id,
                    status_id=status_id,
                    applied_at=now,
                    expires_at=expires_at
                )
                db.add(char_status)
                action = "applied"
            
            db.commit()
            
            return {
                "success": True,
                "character_name": character.name,
                "status_name": status.name,
                "effect_type": status.effect_type.value,
                "applied_at": now.isoformat(),
                "expires_at": expires_at.isoformat(),
                "action": action,
                "message": f"Status '{status.name}' {action} to '{character.name}'"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def populate_location_with_blocks(
        db: Session,
        location_id: int,
        block_configs: List[Dict]
    ) -> Dict:
        """
        Stored Procedure: Populate a location with multiple blocks at once.
        
        Args:
            block_configs: List of dicts with keys: block_type, contains_item_id, properties
        
        Steps:
        1. Validate location exists
        2. Validate all item IDs
        3. Create all blocks
        4. Commit or rollback all
        """
        try:
            # Validate location
            location = db.query(Location).filter(
                Location.location_id == location_id
            ).first()
            if not location:
                return {"success": False, "error": f"Location {location_id} not found"}
            
            # Validate items
            item_ids = [cfg.get('contains_item_id') for cfg in block_configs 
                       if cfg.get('contains_item_id')]
            if item_ids:
                items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
                valid_item_ids = {item.item_id for item in items}
                invalid = set(item_ids) - valid_item_ids
                if invalid:
                    return {
                        "success": False,
                        "error": f"Invalid item IDs: {invalid}"
                    }
            
            # Create blocks
            blocks_created = []
            for config in block_configs:
                block = BlockContainer(
                    location_id=location_id,
                    block_type=config['block_type'],
                    contains_item_id=config.get('contains_item_id'),
                    properties=config.get('properties')
                )
                db.add(block)
                db.flush()
                blocks_created.append({
                    "block_id": block.block_id,
                    "block_type": block.block_type,
                    "contains_item_id": block.contains_item_id
                })
            
            db.commit()
            
            return {
                "success": True,
                "location_name": location.name,
                "blocks_created": len(blocks_created),
                "blocks": blocks_created,
                "message": f"Created {len(blocks_created)} blocks in '{location.name}'"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_chapter_complete_info(db: Session, chapter_id: int) -> Dict:
        """
        Stored Procedure: Get complete information about a chapter.
        
        Returns comprehensive chapter data in one query.
        """
        try:
            chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
            if not chapter:
                return {"success": False, "error": f"Chapter {chapter_id} not found"}
            
            # Get all related data
            locations = db.query(Location).filter(
                Location.chapter_id == chapter_id
            ).all()
            
            bosses = db.query(Boss, Character).join(
                Character, Boss.character_id == Character.character_id
            ).filter(Boss.chapter_id == chapter_id).all()
            
            pixls = db.query(Pixl).filter(
                Pixl.unlock_chapter_id == chapter_id
            ).all()
            
            playable_chars = db.query(PlayableCharacter, Character).join(
                Character, PlayableCharacter.character_id == Character.character_id
            ).filter(PlayableCharacter.unlock_chapter_id == chapter_id).all()
            
            return {
                "success": True,
                "chapter": {
                    "chapter_id": chapter.chapter_id,
                    "name": chapter.name,
                    "world_number": chapter.world_number,
                    "description": chapter.description
                },
                "locations": [
                    {
                        "location_id": loc.location_id,
                        "name": loc.name,
                        "type": loc.type
                    } for loc in locations
                ],
                "bosses": [
                    {
                        "boss_id": boss.boss_id,
                        "name": char.name,
                        "phase_count": boss.phase_count,
                        "special_mechanics": boss.special_mechanics
                    } for boss, char in bosses
                ],
                "pixls": [
                    {
                        "pixl_id": pixl.pixl_id,
                        "name": pixl.name,
                        "ability": pixl.ability,
                        "is_optional": pixl.is_optional
                    } for pixl in pixls
                ],
                "playable_characters": [
                    {
                        "character_id": pc.character_id,
                        "name": char.name,
                        "special_ability": pc.special_ability
                    } for pc, char in playable_chars
                ],
                "statistics": {
                    "total_locations": len(locations),
                    "total_bosses": len(bosses),
                    "total_pixls": len(pixls),
                    "total_playable_characters": len(playable_chars)
                }
            }
            
        except SQLAlchemyError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def transfer_item_between_blocks(
        db: Session,
        from_block_id: int,
        to_block_id: int
    ) -> Dict:
        """
        Stored Procedure: Transfer an item from one block to another.
        
        Steps:
        1. Validate both blocks exist
        2. Check source block has an item
        3. Move item to destination block
        4. Commit or rollback
        """
        try:
            # Get blocks
            from_block = db.query(BlockContainer).filter(
                BlockContainer.block_id == from_block_id
            ).first()
            to_block = db.query(BlockContainer).filter(
                BlockContainer.block_id == to_block_id
            ).first()
            
            if not from_block:
                return {"success": False, "error": f"Source block {from_block_id} not found"}
            if not to_block:
                return {"success": False, "error": f"Destination block {to_block_id} not found"}
            
            if not from_block.contains_item_id:
                return {"success": False, "error": "Source block has no item"}
            
            # Get item info
            item = db.query(Item).filter(
                Item.item_id == from_block.contains_item_id
            ).first()
            
            # Transfer
            item_id = from_block.contains_item_id
            from_block.contains_item_id = None
            to_block.contains_item_id = item_id
            
            db.commit()
            
            return {
                "success": True,
                "item_id": item_id,
                "item_name": item.name if item else "Unknown",
                "from_block_id": from_block_id,
                "to_block_id": to_block_id,
                "message": f"Item transferred from block {from_block_id} to {to_block_id}"
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }


# Convenience functions for easy imports
def create_enemy_with_character(db: Session, **kwargs):
    return StoredProcedures.create_enemy_with_character(db, **kwargs)

def create_boss_with_character(db: Session, **kwargs):
    return StoredProcedures.create_boss_with_character(db, **kwargs)

def create_side_quest_with_characters(db: Session, **kwargs):
    return StoredProcedures.create_side_quest_with_characters(db, **kwargs)

def apply_status_effect_to_character(db: Session, **kwargs):
    return StoredProcedures.apply_status_effect_to_character(db, **kwargs)

def populate_location_with_blocks(db: Session, **kwargs):
    return StoredProcedures.populate_location_with_blocks(db, **kwargs)

def get_chapter_complete_info(db: Session, chapter_id: int):
    return StoredProcedures.get_chapter_complete_info(db, chapter_id)

def transfer_item_between_blocks(db: Session, **kwargs):
    return StoredProcedures.transfer_item_between_blocks(db, **kwargs)
