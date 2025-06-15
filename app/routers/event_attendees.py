"""
EventAttendees:
    - event_id | int not null
    - user_id | int not null
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter(
    prefix="/event-attendees",
    tags=["event-attendees"]
)

@router.post("/", response_model=schemas.EventAttendeeRead)
def create_event_attendee(
    event_attendee: schemas.EventAttendeeCreate,
    db: Session = Depends(get_db)
):
    """Create a new event attendee."""
    # Check if the event exists
    event = crud.event.get(db, event_attendee.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if the user exists
    user = crud.user.get(db, event_attendee.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the attendee already exists
    existing_attendee = db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_attendee.event_id,
        models.EventAttendee.user_id == event_attendee.user_id
    ).first()
    
    if existing_attendee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered for this event"
        )
    
    return crud.event_attendee.create(db, obj_in=event_attendee)

@router.get("/", response_model=List[schemas.EventAttendeeRead])
def read_event_attendees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all event attendees."""
    return crud.event_attendee.get_multi(db, skip=skip, limit=limit)

@router.get("/event/{event_id}", response_model=List[schemas.EventAttendeeRead])
def read_event_attendees_by_event(
    event_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all attendees for a specific event."""
    # Check if the event exists
    event = crud.event.get(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id
    ).offset(skip).limit(limit).all()

@router.get("/user/{user_id}", response_model=List[schemas.EventAttendeeRead])
def read_event_attendees_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all events a specific user is attending."""
    # Check if the user exists
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db.query(models.EventAttendee).filter(
        models.EventAttendee.user_id == user_id
    ).offset(skip).limit(limit).all()

@router.delete("/{event_id}/{user_id}", response_model=schemas.EventAttendeeRead)
def delete_event_attendee(
    event_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Remove a user from an event."""
    event_attendee = db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id,
        models.EventAttendee.user_id == user_id
    ).first()
    
    if not event_attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event attendee not found"
        )
    
    db.delete(event_attendee)
    db.commit()
    return event_attendee