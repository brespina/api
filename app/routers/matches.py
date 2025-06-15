"""
Matches:
    - match_id | int auto-increment primary key
    - date_time | datetime not null
    - team_id | int not null
    - opponent_id | int not null
    - watch_link | varchar(255)
    - result | varchar(20)
    - game_id | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.MatchRead, status_code=status.HTTP_201_CREATED)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    """Create a new match."""
    # Check if team exists
    team = crud.team.get(db, match.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if opponent exists
    opponent = crud.opponent.get(db, match.opponent_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    # Check if game exists
    game = crud.game.get(db, match.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Validate that team's game matches the specified game
    team_game_id = db.query(models.Team.game_id).filter(models.Team.team_id == match.team_id).scalar()
    if team_game_id != match.game_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team's game does not match the specified game"
        )
    
    # Validate that opponent's game matches the specified game
    opponent_game_id = db.query(models.Opponent.game_id).filter(models.Opponent.opponent_id == match.opponent_id).scalar()
    if opponent_game_id != match.game_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Opponent's game does not match the specified game"
        )
    
    return crud.match.create(db, obj_in=match)

@router.get("/{match_id}", response_model=schemas.MatchRead)
def read_match(match_id: int, db: Session = Depends(get_db)):
    """Get a specific match by ID."""
    match = crud.match.get(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match

@router.get("/", response_model=List[schemas.MatchRead])
def list_matches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all matches."""
    return crud.match.get_multi(db, skip=skip, limit=limit)

@router.get("/team/{team_id}", response_model=List[schemas.MatchRead])
def list_team_matches(
    team_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all matches for a specific team."""
    # Check if team exists
    team = crud.team.get(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    return db.query(models.Match).filter(
        models.Match.team_id == team_id
    ).offset(skip).limit(limit).all()

@router.get("/opponent/{opponent_id}", response_model=List[schemas.MatchRead])
def list_opponent_matches(
    opponent_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all matches for a specific opponent."""
    # Check if opponent exists
    opponent = crud.opponent.get(db, opponent_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    return db.query(models.Match).filter(
        models.Match.opponent_id == opponent_id
    ).offset(skip).limit(limit).all()

@router.get("/game/{game_id}", response_model=List[schemas.MatchRead])
def list_game_matches(
    game_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all matches for a specific game."""
    # Check if game exists
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return db.query(models.Match).filter(
        models.Match.game_id == game_id
    ).offset(skip).limit(limit).all()

@router.get("/upcoming", response_model=List[schemas.MatchRead])
def list_upcoming_matches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all upcoming matches."""
    current_time = datetime.utcnow()
    return db.query(models.Match).filter(
        models.Match.date_time > current_time
    ).order_by(models.Match.date_time).offset(skip).limit(limit).all()

@router.get("/past", response_model=List[schemas.MatchRead])
def list_past_matches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all past matches."""
    current_time = datetime.utcnow()
    return db.query(models.Match).filter(
        models.Match.date_time <= current_time
    ).order_by(models.Match.date_time.desc()).offset(skip).limit(limit).all()

@router.put("/{match_id}", response_model=schemas.MatchRead)
def update_match(
    match_id: int,
    match: schemas.MatchCreate,
    db: Session = Depends(get_db)
):
    """Update a match."""
    db_match = crud.match.get(db, match_id)
    if not db_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Check if team exists
    team = crud.team.get(db, match.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if opponent exists
    opponent = crud.opponent.get(db, match.opponent_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    # Check if game exists
    game = crud.game.get(db, match.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Validate that team's game matches the specified game
    team_game_id = db.query(models.Team.game_id).filter(models.Team.team_id == match.team_id).scalar()
    if team_game_id != match.game_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team's game does not match the specified game"
        )
    
    # Validate that opponent's game matches the specified game
    opponent_game_id = db.query(models.Opponent.game_id).filter(models.Opponent.opponent_id == match.opponent_id).scalar()
    if opponent_game_id != match.game_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Opponent's game does not match the specified game"
        )
    
    return crud.match.update(db, db_obj=db_match, obj_in=match.dict())

@router.delete("/{match_id}", response_model=schemas.MatchRead)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    """Delete a match."""
    match = crud.match.get(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    return crud.match.remove(db, obj_id=match_id)