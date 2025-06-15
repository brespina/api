"""
Games:
    - game_id | int auto-increment primary key
    - game_name | varchar(255) not null
    - bg_image | mediumblob not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.GameRead, status_code=status.HTTP_201_CREATED)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    """Create a new game."""
    # Check for duplicate game name
    existing_game = db.query(models.Game).filter(
        models.Game.game_name == game.game_name
    ).first()
    
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this name already exists"
        )
    
    return crud.game.create(db, obj_in=game)

@router.get("/{game_id}", response_model=schemas.GameRead)
def read_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game by ID."""
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

@router.get("/", response_model=List[schemas.GameRead])
def list_games(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all games."""
    return crud.game.get_multi(db, skip=skip, limit=limit)

@router.get("/name/{game_name}", response_model=schemas.GameRead)
def read_game_by_name(game_name: str, db: Session = Depends(get_db)):
    """Get a specific game by name."""
    game = db.query(models.Game).filter(
        models.Game.game_name == game_name
    ).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

@router.put("/{game_id}", response_model=schemas.GameRead)
def update_game(
    game_id: int,
    game: schemas.GameCreate,
    db: Session = Depends(get_db)
):
    """Update a game."""
    db_game = crud.game.get(db, game_id)
    if not db_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check for duplicate game name
    existing_game = db.query(models.Game).filter(
        models.Game.game_id != game_id,
        models.Game.game_name == game.game_name
    ).first()
    
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this name already exists"
        )
    
    return crud.game.update(db, db_obj=db_game, obj_in=game.dict())

@router.delete("/{game_id}", response_model=schemas.GameRead)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    """Delete a game."""
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if game has associated teams or opponents
    if game.teams or game.opponents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete game with associated teams or opponents"
        )
    
    return crud.game.remove(db, obj_id=game_id)
