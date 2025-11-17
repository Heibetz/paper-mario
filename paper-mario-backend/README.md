# Paper Mario Database Backend

This is a SQLAlchemy ORM implementation for a Paper Mario database based on the ERD.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure if needed:
```bash
copy .env.example .env
```

5. Initialize the database:
```bash
python init_db.py
```

## Project Structure

- `models/` - SQLAlchemy model definitions
- `config.py` - Database configuration
- `init_db.py` - Database initialization script
- `seed_data.py` - Sample data seeder

## Features

- **17 Tables** from ERD with proper relationships
- **CHECK Constraints** for data validation (e.g., HP > 0, attack >= 0)
- **UNIQUE Constraints** for data integrity (e.g., unique character names)
- **Indexes** on foreign keys and frequently queried fields
- **ENUM types** for categorical data
- **Foreign Key relationships** with proper cascading
