"""
Opponents:
    - opponent_id | int auto-increment primary key
    - opponent_name | varchar(100) not null
    - game_id | int not null foreign key
    - school | varchar(100) nullable
    - logo | mediumblob nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OpponentRead, status_code=status.HTTP_201_CREATED)
def create_opponent(opponent: schemas.OpponentCreate, db: Session = Depends(get_db)):
    """Create a new opponent."""
    # Check if game exists
    game = crud.game.get(db, opponent.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if opponent name is unique for this game
    existing_opponent = db.query(models.Opponent).filter(
        models.Opponent.game_id == opponent.game_id,
        models.Opponent.opponent_name == opponent.opponent_name
    ).first()
    
    if existing_opponent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Opponent with this name already exists for this game"
        )
    
    return crud.opponent.create(db, obj_in=opponent)

@router.get("/{opponent_id}", response_model=schemas.OpponentRead)
def read_opponent(opponent_id: int, db: Session = Depends(get_db)):
    """Get a specific opponent by ID."""
    opponent = crud.opponent.get(db, opponent_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    return opponent

@router.get("/", response_model=List[schemas.OpponentRead])
def list_opponents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all opponents."""
    return crud.opponent.get_multi(db, skip=skip, limit=limit)

@router.get("/game/{game_id}", response_model=List[schemas.OpponentRead])
def list_game_opponents(
    game_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all opponents for a specific game."""
    # Check if game exists
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return db.query(models.Opponent).filter(
        models.Opponent.game_id == game_id
    ).offset(skip).limit(limit).all()

@router.put("/{opponent_id}", response_model=schemas.OpponentRead)
def update_opponent(
    opponent_id: int,
    opponent: schemas.OpponentCreate,
    db: Session = Depends(get_db)
):
    """Update an opponent."""
    db_opponent = crud.opponent.get(db, opponent_id)
    if not db_opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    # Check if opponent name is unique for this game
    existing_opponent = db.query(models.Opponent).filter(
        models.Opponent.opponent_id != opponent_id,
        models.Opponent.game_id == opponent.game_id,
        models.Opponent.opponent_name == opponent.opponent_name
    ).first()
    
    if existing_opponent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Opponent with this name already exists for this game"
        )
    
    return crud.opponent.update(db, db_obj=db_opponent, obj_in=opponent.dict())

@router.delete("/{opponent_id}", response_model=schemas.OpponentRead)
def delete_opponent(opponent_id: int, db: Session = Depends(get_db)):
    """Delete an opponent."""
    opponent = crud.opponent.get(db, opponent_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    # Check if opponent has associated matches
    if opponent.matches:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete opponent with associated matches"
        )
    
    return crud.opponent.remove(db, obj_id=opponent_id)