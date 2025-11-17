# Database Constraints and Indexes

This document details all CHECK constraints, UNIQUE constraints, and INDEXES implemented in the Paper Mario database.

## CHECK Constraints

CHECK constraints ensure data validity by enforcing business rules at the database level.

### Chapters Table
- **check_world_number_positive**: `world_number > 0`
  - Ensures world numbers are always positive

### Enemies Table
- **check_enemy_hp_positive**: `hp > 0`
  - Enemies must have positive HP
- **check_enemy_attack_non_negative**: `attack >= 0`
  - Attack values cannot be negative
- **check_enemy_defense_non_negative**: `defense >= 0`
  - Defense values cannot be negative
- **check_card_score_non_negative**: `card_score >= 0`
  - Card scores cannot be negative

### Bosses Table
- **check_phase_count_positive**: `phase_count > 0`
  - Bosses must have at least one phase

### Status_Effects Table
- **check_duration_non_negative**: `duration_seconds >= 0`
  - Status effect duration cannot be negative

---

## UNIQUE Constraints

UNIQUE constraints prevent duplicate values in specific columns.

### Characters Table
- **name**: Each character must have a unique name
  - Prevents duplicate character entries

### Chapters Table
- **name**: Each chapter must have a unique name
  - Prevents duplicate chapter entries

### Pixls Table
- **name**: Each pixl must have a unique name
  - Prevents duplicate pixl entries

### Status_Effects Table
- **name**: Each status effect must have a unique name
  - Prevents duplicate status effect entries

### Items Table
- **name**: Each item must have a unique name
  - Prevents duplicate item entries

### Side_Quests Table
- **name**: Each quest must have a unique name
  - Prevents duplicate quest entries

---

## INDEXES

Indexes improve query performance on frequently searched columns.

### Characters Table
- **idx_character_name**: Index on `name`
  - Speeds up character name searches

### Chapters Table
- **idx_chapter_world_number**: Index on `world_number`
  - Speeds up queries filtering by world number

### Playable_Characters Table
- **idx_playable_unlock_chapter**: Index on `unlock_chapter_id` (FK)
  - Speeds up joins with chapters table

### Locations Table
- **idx_location_chapter**: Index on `chapter_id` (FK)
  - Speeds up joins with chapters table
- **idx_location_name**: Index on `name`
  - Speeds up location name searches
- **idx_location_type**: Index on `type`
  - Speeds up filtering by location type

### Pixls Table
- **idx_pixl_unlock_chapter**: Index on `unlock_chapter_id` (FK)
  - Speeds up joins with chapters table
- **idx_pixl_name**: Index on `name`
  - Speeds up pixl name searches

### Status_Effects Table
- **idx_status_name**: Index on `name`
  - Speeds up status effect name searches

### Character_Status_Effects Table (Join Table)
- **idx_char_status_character**: Index on `character_id` (FK)
  - Speeds up queries by character
- **idx_char_status_status**: Index on `status_id` (FK)
  - Speeds up queries by status effect
- **idx_char_status_expires**: Index on `expires_at`
  - Speeds up queries for expired effects

### Enemies Table
- **idx_enemy_character**: Index on `character_id` (FK)
  - Speeds up joins with characters table

### Bosses Table
- **idx_boss_character**: Index on `character_id` (FK)
  - Speeds up joins with characters table
- **idx_boss_chapter**: Index on `chapter_id` (FK)
  - Speeds up joins with chapters table

### Items Table
- **idx_item_name**: Index on `name`
  - Speeds up item name searches
- **idx_item_key_item**: Index on `is_key_item`
  - Speeds up filtering for key items vs regular items

### Objects Table
- **idx_object_location**: Index on `location_id` (FK)
  - Speeds up joins with locations table
- **idx_object_type**: Index on `object_type`
  - Speeds up filtering by object type

### Navigation_Objects Table
- **idx_navobj_location**: Index on `location_id` (FK)
  - Speeds up joins with locations table
- **idx_navobj_type**: Index on `type`
  - Speeds up filtering by navigation type

### Obstacles Table
- **idx_obstacle_location**: Index on `location_id` (FK)
  - Speeds up joins with locations table
- **idx_obstacle_type**: Index on `type`
  - Speeds up filtering by obstacle type

### Blocks_Containers Table
- **idx_block_location**: Index on `location_id` (FK)
  - Speeds up joins with locations table
- **idx_block_item**: Index on `contains_item_id` (FK)
  - Speeds up joins with items table
- **idx_block_type**: Index on `block_type`
  - Speeds up filtering by block type

### Switches Table
- **idx_switch_location**: Index on `location_id` (FK)
  - Speeds up joins with locations table
- **idx_switch_target**: Index on `target_navobj_id` (FK)
  - Speeds up joins with navigation_objects table
- **idx_switch_type**: Index on `switch_type`
  - Speeds up filtering by switch type

### Side_Quests Table
- **idx_quest_location**: Index on `start_location_id` (FK)
  - Speeds up joins with locations table
- **idx_quest_reward**: Index on `reward_item_id` (FK)
  - Speeds up joins with items table
- **idx_quest_name**: Index on `name`
  - Speeds up quest name searches

### Quest_Character Table (Join Table)
- **idx_quest_char_quest**: Index on `quest_id` (FK)
  - Speeds up queries by quest
- **idx_quest_char_character**: Index on `character_id` (FK)
  - Speeds up queries by character
- **idx_quest_char_role**: Index on `role`
  - Speeds up filtering by character role in quest

---

## ENUM Types

The following tables use ENUM types for categorical data:

### Locations Table
- **type**: `LocationType` enum
  - Values: `hub`, `level`, `dungeon`, `other`

### Status_Effects Table
- **effect_type**: `EffectType` enum
  - Values: `buff`, `debuff`

### Navigation_Objects Table
- **type**: `NavigationType` enum
  - Values: `door`, `arrow`, `elevator`, `save_block`, `star_block`, `rift`

### Blocks_Containers Table
- **block_type**: `BlockType` enum
  - Values: `movable`, `breakable`, `save`, `star`

### Quest_Character Table
- **role**: `QuestRole` enum
  - Values: `giver`, `target`, `helper`

---

## Foreign Key Relationships

All foreign keys include proper cascade behavior:

- **CASCADE**: When parent is deleted, child records are also deleted
- **SET NULL**: When parent is deleted, foreign key is set to NULL
- **Indexes**: All foreign keys have corresponding indexes for performance

### Tables with CASCADE DELETE:
- playable_characters → characters
- locations → chapters
- enemies → characters
- bosses → characters, chapters
- character_status_effects → characters, status_effects
- objects → locations
- navigation_objects → locations
- obstacles → locations
- blocks_containers → locations
- switches → locations
- side_quests relationships
- quest_character → side_quests, characters

### Tables with SET NULL:
- playable_characters.unlock_chapter_id → chapters
- pixls.unlock_chapter_id → chapters
- blocks_containers.contains_item_id → items
- switches.target_navobj_id → navigation_objects
- side_quests.start_location_id → locations
- side_quests.reward_item_id → items

---

## Summary

- **Total CHECK Constraints**: 7
- **Total UNIQUE Constraints**: 6
- **Total INDEXES**: 40+
- **Total ENUM Types**: 5
- **Total Tables**: 17
- **Total Foreign Key Relationships**: 20+

This comprehensive constraint and index strategy ensures:
1. Data integrity through validation
2. Prevention of duplicates
3. Optimal query performance
4. Proper relationship management
5. Type safety with ENUMs
