"""
Coordinators:
    - coordinator_id | int auto-increment primary key
    - user_id | int not null foreign key
    - game_id | int not null foreign key
    - start_date | datetime not null
    - end_date | datetime nullable
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.CoordinatorRead, status_code=status.HTTP_201_CREATED)
def create_coordinator(coordinator: schemas.CoordinatorCreate, db: Session = Depends(get_db)):
    """Create a new coordinator."""
    # Check if user exists
    user = crud.user.get(db, coordinator.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if game exists
    game = crud.game.get(db, coordinator.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check for overlapping coordinator periods
    overlapping_coordinator = db.query(models.Coordinator).filter(
        models.Coordinator.user_id == coordinator.user_id,
        models.Coordinator.game_id == coordinator.game_id,
        ((models.Coordinator.start_date <= coordinator.start_date) & 
         (models.Coordinator.end_date >= coordinator.start_date)) |
        ((models.Coordinator.start_date <= coordinator.end_date) & 
         (models.Coordinator.end_date >= coordinator.end_date)) |
        ((models.Coordinator.start_date >= coordinator.start_date) & 
         (models.Coordinator.end_date <= coordinator.end_date))
    ).first()
    
    if overlapping_coordinator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a coordinator for this game during the specified period"
        )
    
    return crud.coordinator.create(db, obj_in=coordinator)

@router.get("/{coordinator_id}", response_model=schemas.CoordinatorRead)
def read_coordinator(coordinator_id: int, db: Session = Depends(get_db)):
    """Get a specific coordinator by ID."""
    coordinator = crud.coordinator.get(db, coordinator_id)
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )
    return coordinator

@router.get("/", response_model=List[schemas.CoordinatorRead])
def list_coordinators(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all coordinators."""
    return crud.coordinator.get_multi(db, skip=skip, limit=limit)

@router.get("/game/{game_id}", response_model=List[schemas.CoordinatorRead])
def list_game_coordinators(
    game_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all coordinators for a specific game."""
    # Check if game exists
    game = crud.game.get(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return db.query(models.Coordinator).filter(
        models.Coordinator.game_id == game_id
    ).offset(skip).limit(limit).all()

@router.put("/{coordinator_id}", response_model=schemas.CoordinatorRead)
def update_coordinator(
    coordinator_id: int,
    coordinator: schemas.CoordinatorCreate,
    db: Session = Depends(get_db)
):
    """Update a coordinator."""
    db_coordinator = crud.coordinator.get(db, coordinator_id)
    if not db_coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )
    
    # Check for overlapping coordinator periods
    overlapping_coordinator = db.query(models.Coordinator).filter(
        models.Coordinator.coordinator_id != coordinator_id,
        models.Coordinator.user_id == coordinator.user_id,
        models.Coordinator.game_id == coordinator.game_id,
        ((models.Coordinator.start_date <= coordinator.start_date) & 
         (models.Coordinator.end_date >= coordinator.start_date)) |
        ((models.Coordinator.start_date <= coordinator.end_date) & 
         (models.Coordinator.end_date >= coordinator.end_date)) |
        ((models.Coordinator.start_date >= coordinator.start_date) & 
         (models.Coordinator.end_date <= coordinator.end_date))
    ).first()
    
    if overlapping_coordinator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a coordinator for this game during the specified period"
        )
    
    return crud.coordinator.update(db, db_obj=db_coordinator, obj_in=coordinator.dict())

@router.delete("/{coordinator_id}", response_model=schemas.CoordinatorRead)
def delete_coordinator(coordinator_id: int, db: Session = Depends(get_db)):
    """Delete a coordinator."""
    coordinator = crud.coordinator.get(db, coordinator_id)
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )
    
    # Check if coordinator has associated teams
    if coordinator.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete coordinator with associated teams"
        )
    
    return crud.coordinator.remove(db, obj_id=coordinator_id)