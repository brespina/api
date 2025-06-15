"""
Teams:
    - team_id | int auto-increment primary key
    - team_name | varchar(100) not null unique
    - game_id | int not null foreign key
    - coordinator_id | int not null foreign key
    - achievements | varchar(255) nullable
    - wins | int not null
    - losses | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    """Create a new team."""
    # Check if game exists
    game = crud.game.get(db, team.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if coordinator exists
    coordinator = crud.coordinator.get(db, team.coordinator_id)
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )
    
    # Check if team name is unique
    existing_team = db.query(models.Team).filter(
        models.Team.team_name == team.team_name
    ).first()
    
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team with this name already exists"
        )
    
    return crud.team.create(db, obj_in=team)

@router.get("/{team_id}", response_model=schemas.TeamRead)
def read_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team by ID."""
    team = crud.team.get(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return team

@router.get("/", response_model=List[schemas.TeamRead])
def list_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams."""
    return crud.team.get_multi(db, skip=skip, limit=limit)

@router.get("/game/{game_id}", response_model=List[schemas.TeamRead])
def list_game_teams(
    game_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams for a specific game."""
    # Check if game exists
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return db.query(models.Team).filter(
        models.Team.game_id == game_id
    ).offset(skip).limit(limit).all()

@router.get("/coordinator/{coordinator_id}", response_model=List[schemas.TeamRead])
def list_coordinator_teams(
    coordinator_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams for a specific coordinator."""
    # Check if coordinator exists
    coordinator = crud.coordinator.get(db, coordinator_id)
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )
    
    return db.query(models.Team).filter(
        models.Team.coordinator_id == coordinator_id
    ).offset(skip).limit(limit).all()

@router.put("/{team_id}", response_model=schemas.TeamRead)
def update_team(
    team_id: int,
    team: schemas.TeamCreate,
    db: Session = Depends(get_db)
):
    """Update a team."""
    db_team = crud.team.get(db, team_id)
    if not db_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if team name is unique
    existing_team = db.query(models.Team).filter(
        models.Team.team_id != team_id,
        models.Team.team_name == team.team_name
    ).first()
    
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team with this name already exists"
        )
    
    return crud.team.update(db, db_obj=db_team, obj_in=team.dict())

@router.delete("/{team_id}", response_model=schemas.TeamRead)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a team."""
    team = crud.team.get(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Check if team has associated matches or team memberships
    if team.matches or team.team_memberships:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete team with associated matches or team memberships"
        )
    
    return crud.team.remove(db, obj_id=team_id)