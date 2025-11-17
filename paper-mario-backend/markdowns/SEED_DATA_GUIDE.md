# 🎮 Super Paper Mario - Comprehensive Seed Data Guide

## Overview

The comprehensive seed data includes **authentic data from the Super Paper Mario wiki**, including all 8 chapters, 4 playable characters, 13 Pixls, 14+ bosses, 15 enemies, 25+ items, 33+ locations, and much more!

## What's Included

### ✅ Complete Game Content

- **8 Chapters**: All worlds from Lineland to Castle Bleck
- **4 Playable Characters**: Mario, Peach, Bowser, and Luigi with accurate abilities
- **13 Pixls**: All Pixls including Tippi, Thoreau, Boomer, Slim, Thudley, Carrie, Fleep, Cudge, Dottie, Barry, Dashell, Piccolo, and Tiptron
- **14 Bosses**: Including O'Chunks, Fracktail, Mimi, Dimentio, Francis, Mr. L, King Croacus, Bonechill, Count Bleck, Super Dimentio, and optional bosses
- **15 Enemies**: Goombas, Koopa Troopas, Hammer Bros, Magikoopas, and more
- **25 Items**: Mushrooms, attack items, status items, and key items
- **33+ Locations**: All major areas from each chapter including Flipside, Flopside, and Pits of 100 Trials
- **10 Status Effects**: Poison, Freeze, Stun, Burn, and more
- **8 Side Quests**: Duel of 100, Pit challenges, and collection quests
- **Blocks**: Question blocks and brick blocks with items

## How to Use

### Option 1: Fresh Start (Recommended for New Database)

```bash
# 1. Initialize database
python init_db.py

# 2. Seed with comprehensive data
python seed_data_comprehensive.py
```

### Option 2: Add to Existing Database

If you already have some data and want to add more:

```bash
# Run the comprehensive seed (it will add to existing data)
python seed_data_comprehensive.py
```

### Option 3: Reset and Reseed

```bash
# Delete the database file
rm paper_mario.db

# Initialize fresh
python init_db.py

# Seed with comprehensive data
python seed_data_comprehensive.py
```

## What's Different from seed_data.py?

| Feature | seed_data.py (Old) | seed_data_comprehensive.py (New) |
|---------|-------------------|----------------------------------|
| Chapters | 3 chapters | **8 chapters** (complete game) |
| Playable Characters | 3 | **4 (+ Luigi!)** |
| Pixls | 2 | **13 (all Pixls!)** |
| Bosses | 1 | **14 (all bosses!)** |
| Enemies | 3 | **15 different types** |
| Locations | 5 | **33+ locations** |
| Items | 3 | **25 items** |
| Side Quests | 1 | **8 quests** |
| Data Source | Sample | **Real wiki data** |

## Example Data

### Chapters
- **Chapter 1: Lineland** - Flat 2D world
- **Chapter 2: Gloam Valley** - Dark mysterious valley  
- **Chapter 3: The Bitlands** - Retro pixelated world
- **Chapter 4: Outer Space** - Space adventure
- **Chapter 5: Land of the Cragnons** - Underground caverns
- **Chapter 6: Sammer's Kingdom** - World of 100 warriors
- **Chapter 7: The Underwhere** - Land of the dead
- **Chapter 8: Castle Bleck** - Final battleground

### Playable Characters (with accurate abilities)
- **Mario**: Flip between 2D and 3D
- **Peach**: Float with parasol
- **Bowser**: Breathe fire
- **Luigi**: Super jump

### All 13 Pixls
- Required: Tippi, Thoreau, Boomer, Slim, Thudley, Carrie, Fleep, Tiptron, Piccolo
- Optional: Cudge, Dottie, Barry, Dashell

### Boss Examples
- **Fracktail** (Ch 1): Robotic dragon
- **Mimi** (Ch 2): Shape-shifting spider
- **King Croacus IV** (Ch 5): 3-phase plant boss
- **Bonechill** (Ch 7): Frozen dragon
- **Super Dimentio** (Ch 8): Final boss

## Testing the Data

After seeding, test it out:

```bash
# Start the API
uvicorn main:app --reload

# Visit the docs
http://127.0.0.1:8000/docs

# Try these endpoints:
GET /chapters          # See all 8 chapters
GET /playable-characters  # See Mario, Peach, Bowser, Luigi
GET /pixls             # See all 13 Pixls
GET /bosses            # See all bosses
GET /locations         # See 33+ locations
GET /queries/chapter-summary/1  # Get complete Chapter 1 info
```

## API Examples

### Get All Chapters
```bash
curl http://localhost:8000/chapters
```

### Get Specific Chapter Details
```bash
curl http://localhost:8000/queries/chapter-summary/1
```

### Get All Pixls
```bash
curl http://localhost:8000/pixls
```

### Get Bosses by Chapter
```bash
curl http://localhost:8000/bosses?chapter_id=1
```

## Notes

- Data is based on the official Super Paper Mario wiki
- All stats, abilities, and descriptions are accurate to the game
- Relationships between entities are properly established
- Optional Pixls are marked correctly
- Boss phase counts and mechanics are included
- All items have proper effects described

## Need to Customize?

Edit `seed_data_comprehensive.py` to:
- Add more enemies
- Add more locations to specific chapters
- Add custom items
- Modify stats
- Add more side quests

Enjoy your comprehensive Super Paper Mario database! 🎮✨
