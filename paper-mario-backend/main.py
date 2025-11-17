"""FastAPI main application for Paper Mario database."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    characters, chapters, enemies, items, side_quests,
    playable_characters, locations, pixls, status_effects,
    bosses, objects, navigation_objects, obstacles,
    blocks_containers, switches
)

# Create FastAPI app
app = FastAPI(
    title="Paper Mario API",
    description="REST API for Paper Mario Super database with characters, chapters, enemies, items, and more!",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(characters.router)
app.include_router(playable_characters.router)
app.include_router(chapters.router)
app.include_router(locations.router)
app.include_router(pixls.router)
app.include_router(status_effects.router)
app.include_router(enemies.router)
app.include_router(bosses.router)
app.include_router(items.router)
app.include_router(objects.router)
app.include_router(navigation_objects.router)
app.include_router(obstacles.router)
app.include_router(blocks_containers.router)
app.include_router(switches.router)
app.include_router(side_quests.router)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Paper Mario API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        "total_endpoints": 15,
        "endpoints": {
            "characters": "/characters",
            "playable_characters": "/playable-characters",
            "chapters": "/chapters",
            "locations": "/locations",
            "pixls": "/pixls",
            "status_effects": "/status-effects",
            "enemies": "/enemies",
            "bosses": "/bosses",
            "items": "/items",
            "objects": "/objects",
            "navigation_objects": "/navigation-objects",
            "obstacles": "/obstacles",
            "blocks": "/blocks",
            "switches": "/switches",
            "side_quests": "/side-quests"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
