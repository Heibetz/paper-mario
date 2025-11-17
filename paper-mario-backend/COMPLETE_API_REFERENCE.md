# Complete Paper Mario API Reference

## 🎉 All 15 Endpoint Collections

### 1. **Characters** (`/characters`)
Base character data for all game characters.
- `GET /characters` - List all characters
- `GET /characters/{id}` - Get specific character
- `POST /characters` - Create character
- `PUT /characters/{id}` - Update character
- `DELETE /characters/{id}` - Delete character

### 2. **Playable Characters** (`/playable-characters`)
Characters that can be controlled by the player.
- `GET /playable-characters` - List all playable characters
- `GET /playable-characters/{id}` - Get specific playable character
- `POST /playable-characters` - Create playable character
- `PUT /playable-characters/{id}` - Update playable character
- `DELETE /playable-characters/{id}` - Delete playable character

### 3. **Chapters** (`/chapters`)
Game chapters/worlds.
- `GET /chapters` - List all chapters
- `GET /chapters/{id}` - Get specific chapter
- `GET /chapters/{id}/locations` - Get all locations in chapter
- `POST /chapters` - Create chapter
- `PUT /chapters/{id}` - Update chapter
- `DELETE /chapters/{id}` - Delete chapter

**Validation**: `world_number` must be > 0

### 4. **Locations** (`/locations`)
Game areas and places.
- `GET /locations?location_type=hub&chapter_id=1` - List locations with filters
- `GET /locations/{id}` - Get specific location
- `POST /locations` - Create location
- `PUT /locations/{id}` - Update location
- `DELETE /locations/{id}` - Delete location

**Query Filters**:
- `location_type`: hub, level, dungeon, other
- `chapter_id`: Filter by chapter

### 5. **Pixls** (`/pixls`)
Pixl companions.
- `GET /pixls?optional_only=true` - List pixls with filters
- `GET /pixls/{id}` - Get specific pixl
- `POST /pixls` - Create pixl
- `PUT /pixls/{id}` - Update pixl
- `DELETE /pixls/{id}` - Delete pixl

**Query Filters**:
- `optional_only`: true/false

### 6. **Status Effects** (`/status-effects`)
Buffs and debuffs.
- `GET /status-effects?effect_type=buff` - List status effects
- `GET /status-effects/{id}` - Get specific status effect
- `POST /status-effects` - Create status effect
- `PUT /status-effects/{id}` - Update status effect
- `DELETE /status-effects/{id}` - Delete status effect
- `POST /status-effects/apply` - Apply status to character
- `GET /status-effects/character/{id}` - Get character's active effects

**Query Filters**:
- `effect_type`: buff, debuff

**Validation**: `duration_seconds` must be ≥ 0

### 7. **Enemies** (`/enemies`)
Enemy characters with stats.
- `GET /enemies?min_hp=10&max_hp=50` - List enemies with HP filters
- `GET /enemies/{id}` - Get specific enemy
- `GET /enemies/{id}/character` - Get enemy's character info
- `POST /enemies` - Create enemy
- `PUT /enemies/{id}` - Update enemy stats
- `DELETE /enemies/{id}` - Delete enemy

**Query Filters**:
- `min_hp`: Minimum HP value
- `max_hp`: Maximum HP value

**Validation**: 
- `hp` must be > 0
- `attack`, `defense`, `card_score` must be ≥ 0

### 8. **Bosses** (`/bosses`)
Boss characters.
- `GET /bosses?chapter_id=1` - List bosses with filters
- `GET /bosses/{id}` - Get specific boss
- `GET /bosses/{id}/character` - Get boss's character info
- `POST /bosses` - Create boss
- `PUT /bosses/{id}` - Update boss
- `DELETE /bosses/{id}` - Delete boss

**Query Filters**:
- `chapter_id`: Filter by chapter

**Validation**: `phase_count` must be > 0

### 9. **Items** (`/items`)
Game items and collectibles.
- `GET /items?key_items_only=true` - List items with filters
- `GET /items/{id}` - Get specific item
- `POST /items` - Create item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

**Query Filters**:
- `key_items_only`: true/false

### 10. **Objects** (`/objects`)
Interactive objects in locations.
- `GET /objects?location_id=1&object_type=container` - List objects
- `GET /objects/{id}` - Get specific object
- `POST /objects` - Create object
- `PUT /objects/{id}` - Update object
- `DELETE /objects/{id}` - Delete object

**Query Filters**:
- `location_id`: Filter by location
- `object_type`: Filter by type

### 11. **Navigation Objects** (`/navigation-objects`)
Doors, elevators, save blocks, etc.
- `GET /navigation-objects?location_id=1&nav_type=door` - List nav objects
- `GET /navigation-objects/{id}` - Get specific nav object
- `POST /navigation-objects` - Create nav object
- `PUT /navigation-objects/{id}` - Update nav object
- `DELETE /navigation-objects/{id}` - Delete nav object

**Query Filters**:
- `location_id`: Filter by location
- `nav_type`: door, arrow, elevator, save_block, star_block, rift

### 12. **Obstacles** (`/obstacles`)
Hazards and barriers in locations.
- `GET /obstacles?location_id=1&obstacle_type=spikes` - List obstacles
- `GET /obstacles/{id}` - Get specific obstacle
- `POST /obstacles` - Create obstacle
- `PUT /obstacles/{id}` - Update obstacle
- `DELETE /obstacles/{id}` - Delete obstacle

**Query Filters**:
- `location_id`: Filter by location
- `obstacle_type`: Filter by type

### 13. **Blocks & Containers** (`/blocks`)
Breakable blocks and item containers.
- `GET /blocks?location_id=1&block_type=save&has_item=true` - List blocks
- `GET /blocks/{id}` - Get specific block
- `POST /blocks` - Create block
- `PUT /blocks/{id}` - Update block
- `DELETE /blocks/{id}` - Delete block

**Query Filters**:
- `location_id`: Filter by location
- `block_type`: movable, breakable, save, star
- `has_item`: true/false

### 14. **Switches** (`/switches`)
Switches that control navigation objects.
- `GET /switches?location_id=1&switch_type=pressure_plate` - List switches
- `GET /switches/{id}` - Get specific switch
- `POST /switches` - Create switch
- `PUT /switches/{id}` - Update switch
- `DELETE /switches/{id}` - Delete switch

**Query Filters**:
- `location_id`: Filter by location
- `switch_type`: Filter by type

### 15. **Side Quests** (`/side-quests`)
Optional quests.
- `GET /side-quests` - List all side quests
- `GET /side-quests/{id}` - Get specific quest
- `POST /side-quests` - Create quest
- `PUT /side-quests/{id}` - Update quest
- `DELETE /side-quests/{id}` - Delete quest

---

## 🔧 Common Features

### Pagination
All list endpoints support:
```
?skip=0&limit=100
```

### Response Codes
- `200 OK` - Successful GET/PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error or duplicate
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Invalid data

### Automatic Validation
All endpoints have:
✅ Request validation via Pydantic
✅ Response validation
✅ UNIQUE constraint checking
✅ CHECK constraint enforcement
✅ Foreign key validation

---

## 🚀 Quick Start

```bash
# Start the server
uvicorn main:app --reload

# Access interactive docs
# http://127.0.0.1:8000/docs

# Test an endpoint
curl http://127.0.0.1:8000/characters
```

---

## 📊 Database Stats

- **Total Tables**: 17
- **Total API Endpoints**: 15 collections, 75+ individual endpoints
- **CHECK Constraints**: 7
- **UNIQUE Constraints**: 6
- **Indexes**: 40+
- **ENUM Types**: 5
- **Foreign Key Relationships**: 20+

---

## 💡 Example Workflows

### Create a Complete Enemy
```bash
# 1. Create character
POST /characters
{
  "name": "Goomba",
  "description": "A common enemy"
}

# 2. Create enemy with stats
POST /enemies
{
  "character_id": 1,
  "hp": 10,
  "attack": 1,
  "defense": 0,
  "card_score": 5
}
```

### Query Chapter with Locations
```bash
# Get chapter 1
GET /chapters/1

# Get all locations in chapter 1
GET /chapters/1/locations

# Or filter locations directly
GET /locations?chapter_id=1&location_type=dungeon
```

### Find Enemies by HP Range
```bash
# Get all enemies with HP between 10 and 50
GET /enemies?min_hp=10&max_hp=50
```

### Apply Status Effect
```bash
# Apply poison to character 1
POST /status-effects/apply
{
  "character_id": 1,
  "status_id": 2,
  "expires_at": "2025-11-17T20:00:00Z"
}

# Check character's active effects
GET /status-effects/character/1
```

---

## 🎯 Next Steps

1. Test all endpoints at `/docs`
2. Add authentication (JWT tokens)
3. Add more complex queries
4. Build a frontend application
5. Add real-time features with WebSockets
6. Deploy to production

Happy coding! 🎮
