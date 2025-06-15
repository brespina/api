from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, crud
from ..deps import get_db

router = APIRouter()


@router.post("/", response_model=schemas.EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_in: schemas.EventCreate, db: Session = Depends(get_db)):
    # Simple duplicate-email guard
    if db.query(models.Event).filter(models.Event.title == event_in.title).first():
        raise HTTPException(status_code=400, detail="Event already registered")

    return crud.event.create(db, obj_in=event_in)


@router.get("/{event_id}", response_model=schemas.EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.event.get(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/", response_model=list[schemas.EventRead])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.event.get_multi(db, skip=skip, limit=limit)


@router.delete("/{event_id}", response_model=schemas.EventRead)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    return crud.event.remove(db, obj_id=event_id)
