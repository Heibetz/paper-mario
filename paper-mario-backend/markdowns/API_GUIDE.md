# Paper Mario API Guide

## 🚀 Getting Started

### 1. Install Dependencies

```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Install FastAPI and dependencies
pip install -r requirements.txt
```

### 2. Initialize Database (if not done already)

```bash
python init_db.py
python seed_data.py  # Optional: Add sample data
```

### 3. Run the API Server

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload

# Option 2: Using Python
python main.py
```

The server will start at: **http://127.0.0.1:8000**

### 4. Access Interactive Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📡 API Endpoints

### Characters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/characters` | List all characters (paginated) |
| GET | `/characters/{id}` | Get specific character |
| POST | `/characters` | Create new character |
| PUT | `/characters/{id}` | Update character |
| DELETE | `/characters/{id}` | Delete character |

**Example Request:**
```bash
# Get all characters
curl http://localhost:8000/characters

# Create a character
curl -X POST http://localhost:8000/characters \
  -H "Content-Type: application/json" \
  -d '{"name": "Tippi", "description": "A Pixl companion"}'
```

### Chapters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chapters` | List all chapters |
| GET | `/chapters/{id}` | Get specific chapter |
| GET | `/chapters/{id}/locations` | Get all locations in chapter |
| POST | `/chapters` | Create new chapter |
| PUT | `/chapters/{id}` | Update chapter |
| DELETE | `/chapters/{id}` | Delete chapter |

**Example Request:**
```bash
# Get chapter locations
curl http://localhost:8000/chapters/1/locations
```

### Enemies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/enemies` | List all enemies (with HP filters) |
| GET | `/enemies/{id}` | Get specific enemy |
| GET | `/enemies/{id}/character` | Get character info for enemy |
| POST | `/enemies` | Create new enemy |
| PUT | `/enemies/{id}` | Update enemy stats |
| DELETE | `/enemies/{id}` | Delete enemy |

**Query Parameters:**
- `min_hp`: Filter enemies with HP >= value
- `max_hp`: Filter enemies with HP <= value

**Example Request:**
```bash
# Get enemies with HP between 10 and 50
curl "http://localhost:8000/enemies?min_hp=10&max_hp=50"
```

### Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get specific item |
| POST | `/items` | Create new item |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

**Query Parameters:**
- `key_items_only`: Filter for key items (true/false)

**Example Request:**
```bash
# Get only key items
curl "http://localhost:8000/items?key_items_only=true"
```

### Side Quests

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/side-quests` | List all side quests |
| GET | `/side-quests/{id}` | Get specific quest |
| POST | `/side-quests` | Create new quest |
| PUT | `/side-quests/{id}` | Update quest |
| DELETE | `/side-quests/{id}` | Delete quest |

## 🔧 Common Query Parameters

Most list endpoints support:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)

**Example:**
```bash
curl "http://localhost:8000/characters?skip=10&limit=5"
```

## 📝 Request/Response Examples

### Create a Character

**Request:**
```json
POST /characters
{
  "name": "Count Bleck",
  "description": "Main antagonist of Super Paper Mario"
}
```

**Response (201 Created):**
```json
{
  "character_id": 8,
  "name": "Count Bleck",
  "description": "Main antagonist of Super Paper Mario"
}
```

### Create an Enemy

**Request:**
```json
POST /enemies
{
  "character_id": 5,
  "hp": 10,
  "attack": 1,
  "defense": 0,
  "card_score": 5
}
```

**Response (201 Created):**
```json
{
  "enemy_id": 3,
  "character_id": 5,
  "hp": 10,
  "attack": 1,
  "defense": 0,
  "card_score": 5
}
```

### Update an Item

**Request:**
```json
PUT /items/1
{
  "effect": "Restores 15 HP"
}
```

**Response (200 OK):**
```json
{
  "item_id": 1,
  "name": "Mushroom",
  "is_key_item": false,
  "effect": "Restores 15 HP"
}
```

## ⚠️ Error Responses

### 404 Not Found
```json
{
  "detail": "Character with id 999 not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Character with name 'Mario' already exists"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "hp"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

## 🎯 Next Steps

1. **Test the API**: Use the interactive docs at `/docs`
2. **Add more endpoints**: Locations, Pixls, Bosses, etc.
3. **Add authentication**: Protect certain endpoints
4. **Build a frontend**: Create a React/Vue app that uses this API
5. **Add search**: Full-text search for characters and items
6. **Add filtering**: More advanced filtering options

## 💡 Tips

- Use the **Swagger UI** (`/docs`) to test endpoints interactively
- All validation is automatic thanks to Pydantic
- UNIQUE constraints are enforced (character names, item names, etc.)
- CHECK constraints ensure data integrity (HP > 0, etc.)
- Foreign key relationships are maintained automatically
