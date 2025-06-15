"""
Events:
    - event_id | int auto-increment primary key
    - title | varchar(255) not null
    - description | text not null
    - location | varchar(255) not null
    - date_time | datetime not null
    - end_time | datetime not null
    - attendance | int not null
    - created_by_officer_id | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event."""
    # Check if officer exists
    officer = crud.officer.get(db, event.created_by_officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    # Validate event times
    if event.date_time >= event.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    # Check for duplicate event title
    existing_event = db.query(models.Event).filter(
        models.Event.title == event.title
    ).first()
    
    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event with this title already exists"
        )
    
    return crud.event.create(db, obj_in=event)

@router.get("/{event_id}", response_model=schemas.EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID."""
    event = crud.event.get(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.get("/", response_model=List[schemas.EventRead])
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all events."""
    return crud.event.get_multi(db, skip=skip, limit=limit)

@router.get("/officer/{officer_id}", response_model=List[schemas.EventRead])
def list_officer_events(
    officer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all events created by a specific officer."""
    # Check if officer exists
    officer = crud.officer.get(db, officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    return db.query(models.Event).filter(
        models.Event.created_by_officer_id == officer_id
    ).offset(skip).limit(limit).all()

@router.get("/upcoming", response_model=List[schemas.EventRead])
def list_upcoming_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all upcoming events."""
    current_time = datetime.utcnow()
    return db.query(models.Event).filter(
        models.Event.date_time > current_time
    ).order_by(models.Event.date_time).offset(skip).limit(limit).all()

@router.get("/past", response_model=List[schemas.EventRead])
def list_past_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all past events."""
    current_time = datetime.utcnow()
    return db.query(models.Event).filter(
        models.Event.end_time <= current_time
    ).order_by(models.Event.date_time.desc()).offset(skip).limit(limit).all()

@router.put("/{event_id}", response_model=schemas.EventRead)
def update_event(
    event_id: int,
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    """Update an event."""
    db_event = crud.event.get(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if officer exists
    officer = crud.officer.get(db, event.created_by_officer_id)
    if not officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Officer not found"
        )
    
    # Validate event times
    if event.date_time >= event.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    # Check for duplicate event title
    existing_event = db.query(models.Event).filter(
        models.Event.event_id != event_id,
        models.Event.title == event.title
    ).first()
    
    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event with this title already exists"
        )
    
    return crud.event.update(db, db_obj=db_event, obj_in=event.dict())

@router.delete("/{event_id}", response_model=schemas.EventRead)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event."""
    event = crud.event.get(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return crud.event.remove(db, obj_id=event_id)
